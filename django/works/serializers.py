"""
Works serializers.
"""

from rest_framework import serializers

from works.models import TCCWork, WorkStep


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
