"""
Works serializers.
"""

from rest_framework import serializers

from works.models import FinalWork, FinalWorkStage, FinalWorkVersion, ChangeRequest, VersionContentImage

from users.serializers import UserSerializer

from timetables.serializers import StageSerializer


class FinalWorkSerializer(serializers.ModelSerializer):
    """
    Final work serializer.
    """
    mentees_detail = UserSerializer(many=True, source='mentees', read_only=True)
    supervisor_detail = UserSerializer(many=False, source='supervisor', read_only=True)
    current_stage = serializers.SerializerMethodField()

    class Meta:
        model = FinalWork
        fields = ['id', 'description', 'approved', 'supervisor', 'mentees', 'archived', 'mentees_detail',
                  'current_stage', 'supervisor_detail']

    def get_current_stage(self, obj):
        current_stage = obj.get_current_stage()

        if current_stage:
            return FinalWorkStageSerializer(current_stage).data

        return None


class FinalWorkStageSerializer(serializers.ModelSerializer):
    """
    Final work stage serializer.
    """
    stage_detail = StageSerializer(many=False, source='stage', read_only=True)

    class Meta:
        model = FinalWorkStage
        fields = ['id', 'presented', 'status', 'stage', 'final_work', 'stage_detail']


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
