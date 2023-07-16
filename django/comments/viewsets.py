"""
Comments viewsets.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from comments.models import Comment
from comments.serializers import CommentSerializer

from core.permissions import UserGroup


class CommentViewSet(viewsets.ModelViewSet):
    """
    Comment viewset provides all http request methods.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    model = Comment
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset =super().get_queryset()

        user_group = UserGroup(self.request.user)

        if user_group.is_supervisor():
            queryset = queryset.filter(work_stage__final_work__supervisor=self.request.user)

        if user_group.is_mentee():
            queryset = queryset.filter(work_stage__final_work__mentees__in=[self.request.user])

        no_page = self.request.query_params.get('no_page')
        if no_page:
            self.pagination_class = None

        queryset = queryset.order_by('-created_at')

        return queryset
