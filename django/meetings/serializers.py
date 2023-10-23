"""
Implementação dos Serializers do app de meetings.

Contém os serializers para:
    - ApprovedMeetingSerializer (Pivô);
    - MeetingSerializer (Reunião);
"""

from rest_framework import serializers

from meetings.models import Meeting, ApprovedMeeting

from users.serializers import UserSerializer
from users.models import User

from notifications.utils import send_notification
from notifications.tasks import send_mail


class ApprovedMeetingSerializer(serializers.ModelSerializer):
    """Serializer da tabela pivô de reunião e usuário."""
    user_detail = UserSerializer(many=False, read_only=True, source='user')

    class Meta:
        model = ApprovedMeeting
        fields = ['id', 'approved', 'user', 'user_detail']


class MeetingSerializer(serializers.ModelSerializer):
    """Serializer de Reunião."""
    created_at_formated = serializers.SerializerMethodField(read_only=True)
    participants = ApprovedMeetingSerializer(many=True, read_only=True, source='meeting_approved')
    is_approved = serializers.SerializerMethodField(read_only=True)
    meeting_approved = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(), required=False, many=True)
    meeting_date_formated = serializers.SerializerMethodField()
    required_review = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = [
            'id', 'description', 'work_stage', 'meeting_approved', 'participants', 'created_at',
            'created_at_formated', 'meeting_date', 'meeting_date_formated', 'is_approved', 'required_review',
            'developed_activities', 'instructions',
        ]

    def get_created_at_formated(self, obj):
        """Retorna o datetime de criação da reunião."""
        return obj.get_created_at()

    def get_is_approved(self, obj):
        """Retorna o estado de aprovação da reunião."""
        return obj.get_is_approved()

    def get_meeting_date_formated(self, obj):
        """Retorna o datetime da reunião."""
        return obj.get_meeting_date()

    def get_required_review(self, obj):
        """Verifica se um usuário precisa aprovar/desaprovar a reunião."""
        return obj.review_meeting_required(self.context['request'].user)

    def create(self, validated_data):
        """Cria a reunião a partir do endpoint.

        Ao criar uma reunião todos os envolvidos, com exceção do autor
        receberão uma notificação/email.
        """
        meeting = super().create(validated_data)

        mentees = meeting.work_stage.final_work.mentees.all()
        supervisor = meeting.work_stage.final_work.supervisor
        receivers = []

        author = self.context['request'].user

        for mentee in mentees:
            if mentee == author:
                ApprovedMeeting.objects.create(meeting=meeting, user=mentee, approved=True)
            else:
                ApprovedMeeting.objects.create(meeting=meeting, user=mentee, approved=None)
                receivers.append(mentee)

        if supervisor == author:
            ApprovedMeeting.objects.create(meeting=meeting, user=supervisor, approved=True)
        else:
            ApprovedMeeting.objects.create(meeting=meeting, user=supervisor, approved=None)
            receivers.append(supervisor)

        description = (
            f'Uma reunião foi solicitada por: "{author.get_full_name()}", durante a ' \
            f'etapa: "{meeting.work_stage.stage.description}".'
        )

        send_notification(
            description=description,
            author=None,
            receivers=receivers
        )

        send_mail.delay(
            description,
            'Requisição de reunião',
            [{
                'name': receiver.get_full_name(),
                'email': receiver.email,
            } for receiver in receivers],
        )

        return meeting
