"""
Comments serializers.
"""

from rest_framework import serializers

from comments.models import Comment

from users.serializers import UserSerializer

from core.permissions import UserGroup

from notifications.utils import send_notification


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment Serializer.
    """
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author_detail = UserSerializer(many=False, source='author', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'created_at', 'work_stage', 'author', 'author_detail']

    def validate_work_stage(self, work_stage):
        user = self.context['request'].user
        user_group = UserGroup(user)

        if not user_group.is_teacher():
            is_supervisor = user == work_stage.final_work.supervisor
            is_mentee = work_stage.final_work.mentees.all().filter(id__in=[user.id]).exists()

            if not is_supervisor and not is_mentee:
                raise serializers.ValidationError('It is not possible to create a comment without a link to the tcc.')

        return work_stage

    def create(self, request, *args, **kwargs):
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

        send_notification(
            description=f'Um comentário foi feito por: "{author.get_full_name()}", durante a ' \
                        f'etapa: "{comment.work_stage.stage.description}".',
            author=author,
            receivers=receivers
        )

        return comment
