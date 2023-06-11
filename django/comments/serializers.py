"""
Comments serializers.
"""

from rest_framework import serializers

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment Serializer.
    """

    class Meta:
        model = Comment
        fields = '__all__'
