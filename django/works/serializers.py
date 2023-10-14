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
    title = serializers.CharField(
        max_length=128,
        required=True,
    )

    class Meta:
        model = FinalWork
        fields = [
            'id', 'title', 'description', 'approved', 'completed', 'supervisor', 'mentees', 'archived',
            'mentees_detail', 'current_stage', 'supervisor_detail', 'able_to_present', 'grading_score',
        ]

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
    work_stage_detail = FinalWorkStageSerializer(many=False, read_only=True, source='work_stage')
    requester_detail = UserSerializer(many=False, read_only=True, source='requester')
    final_work = serializers.SerializerMethodField()
    created_at_formated = serializers.SerializerMethodField()
    requester = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ChangeRequest
        fields = '__all__'

    def get_final_work(self, obj):
        return obj.work_stage.final_work.title

    def get_created_at_formated(self, obj):
        return obj.get_created_at()

    def update(self, instance, validated_data):
        instance.approved = validated_data.get('approved', None)
        instance.save()
        return instance
