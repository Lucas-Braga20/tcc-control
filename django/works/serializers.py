"""
Works serializers.
"""

from rest_framework import serializers

from works.models import TCCWork, WorkStep, WorkStepVersion, ChangeRequest, Comment


class TCCWorkSerializer(serializers.ModelSerializer):
    """
    TCCWork Serializer.
    """

    class Meta:
        model = TCCWork
        fields = '__all__'


class WorkStepSerializer(serializers.ModelSerializer):
    """
    WorkStep Serializer.
    """

    class Meta:
        model = WorkStep
        fields = '__all__'


class WorkStepVersionSerializer(serializers.ModelSerializer):
    """
    WorkStepVersion Serializer.
    """

    class Meta:
        model = WorkStepVersion
        fields = '__all__'


class ChangeRequestSerializer(serializers.ModelSerializer):
    """
    ChangeRequest Serializer.
    """

    class Meta:
        model = ChangeRequest
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment Serializer.
    """

    class Meta:
        model = Comment
        fields = '__all__'
