"""
Works serializers.
"""

from rest_framework import serializers

from works.models import FinalWork, FinalWorkStage, FinalWorkVersion, ChangeRequest, VersionContentImage


class FinalWorkSerializer(serializers.ModelSerializer):
    """
    Final work serializer.
    """

    class Meta:
        model = FinalWork
        fields = '__all__'


class FinalWorkStageSerializer(serializers.ModelSerializer):
    """
    Final work stage serializer.
    """

    class Meta:
        model = FinalWorkStage
        fields = '__all__'


class FinalWorkVersionSerializer(serializers.ModelSerializer):
    """
    Final work version Serializer.
    """

    class Meta:
        model = FinalWorkVersion
        fields = '__all__'


class VersionContentImageSerializer(serializers.ModelSerializer):
    """
    Version content image serializer.
    """

    class Meta:
        model = VersionContentImage
        fields = ['image', 'version']


class ChangeRequestSerializer(serializers.ModelSerializer):
    """
    Change request serializer.
    """

    class Meta:
        model = ChangeRequest
        fields = '__all__'
