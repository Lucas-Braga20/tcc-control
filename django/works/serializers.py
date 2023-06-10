"""
Works serializers.
"""

from rest_framework import serializers

from works.models import TCCWork, WorkStep, WorkStepVersion


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
