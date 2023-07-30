"""
Metting serializers.
"""

from rest_framework import serializers

from meetings.models import Meeting, ApprovedMeeting

from users.serializers import UserSerializer
from users.models import User

from notifications.utils import send_notification


class ApprovedMeetingSerializer(serializers.ModelSerializer):
    """
    Approved Meeting Serializer.
    """
    user_detail = UserSerializer(many=False, read_only=True, source='user')

    class Meta:
        model = ApprovedMeeting
        fields = ['id', 'approved', 'user', 'user_detail']


class MeetingSerializer(serializers.ModelSerializer):
    """
    Meeting Serializer.
    """
    created_at_formated = serializers.SerializerMethodField(read_only=True)
    participants = ApprovedMeetingSerializer(many=True, read_only=True, source='meeting_approved')
    is_approved = serializers.SerializerMethodField(read_only=True)
    meeting_approved = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(), required=False, many=True)
    meeting_date_formated = serializers.SerializerMethodField()
    required_review = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = ['id', 'description', 'work_stage', 'meeting_approved', 'participants', 'created_at',
                  'created_at_formated', 'meeting_date', 'meeting_date_formated', 'is_approved', 'required_review']

    def get_created_at_formated(self, obj):
        return obj.get_created_at()

    def get_is_approved(self, obj):
        return obj.get_is_approved()

    def get_meeting_date_formated(self, obj):
        return obj.get_meeting_date()

    def get_required_review(self, obj):
        return obj.review_meeting_required(self.context['request'].user)

    def create(self, validated_data):
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
            receivers.append(mentee)

        send_notification(
            description=f'Uma reunião foi solicitada por: "{author.get_full_name()}", durante a ' \
                        f'etapa: "{meeting.work_stage.stage.description}".',
            author=None,
            receivers=receivers
        )

        return meeting
