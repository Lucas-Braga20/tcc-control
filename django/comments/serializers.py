"""
Implementação dos Serializers do app de comments.

Contém os serializers para:
    - CommentSerializer (Comentários);
"""

from rest_framework import serializers

from comments.models import Comment

from users.serializers import UserSerializer

from notifications.utils import send_notification
from notifications.tasks import send_mail


class CommentSerializer(serializers.ModelSerializer):
    """Serializer de Comentário."""
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author_detail = UserSerializer(many=False, source='author', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'created_at', 'work_stage', 'author', 'author_detail']

    def validate_work_stage(self, work_stage):
        """Valida o campo work stage.

        Apenas é possível criar um comentário se o usuário
        for membro do TCC.

        Está validação é feita a partir do campo work stage.
        """
        user = self.context['request'].user

        is_supervisor = user == work_stage.final_work.supervisor
        is_mentee = work_stage.final_work.mentees.all().filter(id__in=[user.id]).exists()
        is_teacher = user.id == work_stage.final_work.timetable.teacher.id

        if not is_supervisor and not is_mentee and not is_teacher:
            raise serializers.ValidationError('O comentário só pode ser feito por um membro do TCC.')

        return work_stage

    def create(self, request, *args, **kwargs):
        """Método de criação do serializer.

        Ao criar um comentário, todos os envolvidos com exceção
        do autor receberão uma notificação/email.
        """
        comment = super().create(request, *args, **kwargs)

        mentees = comment.work_stage.final_work.mentees.all()
        supervisor = comment.work_stage.final_work.supervisor

        receivers = []
        author = self.context['request'].user

        for mentee in mentees:
            if mentee != author:
                receivers.append(mentee)

        if supervisor != author:
            receivers.append(supervisor)

        description = (
            f'Um comentário foi feito por: "{author.get_full_name()}", durante a ' \
            f'etapa: "{comment.work_stage.stage.description}".'
        )

        send_notification(
            description=description,
            author=author,
            receivers=receivers
        )

        send_mail.delay(
            description,
            'Envio de Comentário',
            [{
                'name': receiver.get_full_name(),
                'email': receiver.email,
            } for receiver in receivers],
        )

        return comment
