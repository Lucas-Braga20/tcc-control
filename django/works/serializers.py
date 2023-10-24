"""
Implementação dos Serializers do app de works.

Contém os serializers para:
    - FinalWorkSerializer (TCC);
    - FinalWorkStageSerializer (Etapa);
    - FinalWorkVersionSerializer (Versão);
    - VersionContentImageSerializer (Imagem da versão);
    - ChangeRequestSerializer (Pedido de alteração);
"""

from rest_framework import serializers

from works.models import FinalWork, FinalWorkStage, FinalWorkVersion, ChangeRequest, VersionContentImage

from users.serializers import UserSerializer

from timetables.serializers import StageSerializer


class FinalWorkSerializer(serializers.ModelSerializer):
    """Serializer de TCC."""
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
        """Recupera a etapa atual."""
        current_stage = obj.get_current_stage()

        if current_stage:
            return FinalWorkStageSerializer(current_stage).data

        return None


class FinalWorkStageSerializer(serializers.ModelSerializer):
    """Serializer de Etapa do TCC."""
    stage_detail = StageSerializer(many=False, source='stage', read_only=True)

    class Meta:
        model = FinalWorkStage
        fields = ['id', 'presented', 'status', 'stage', 'final_work', 'stage_detail']


class FinalWorkVersionSerializer(serializers.ModelSerializer):
    """Serializer de Versão da Etapa do TCC."""

    class Meta:
        model = FinalWorkVersion
        fields = '__all__'


class VersionContentImageSerializer(serializers.ModelSerializer):
    """Serializer de Imagem da Versão da Etapa do TCC."""

    class Meta:
        model = VersionContentImage
        fields = ['image', 'version']


class ChangeRequestSerializer(serializers.ModelSerializer):
    """Serializer do pedido de alteração."""
    work_stage_detail = FinalWorkStageSerializer(many=False, read_only=True, source='work_stage')
    requester_detail = UserSerializer(many=False, read_only=True, source='requester')
    final_work = serializers.SerializerMethodField()
    created_at_formated = serializers.SerializerMethodField()
    requester = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ChangeRequest
        fields = '__all__'

    def get_final_work(self, obj):
        """Recupera o TCC."""
        return obj.work_stage.final_work.title

    def get_created_at_formated(self, obj):
        """Recupera a data de criação."""
        return obj.get_created_at()

    def update(self, instance, validated_data):
        """Método de atualização."""
        instance.approved = validated_data.get('approved', None)
        instance.save()
        return instance
