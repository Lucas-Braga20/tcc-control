"""
Comments viewsets.
"""

from rest_framework import viewsets

from comments.models import Comment
from comments.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Comment viewset provides all http request methods.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    model = Comment
