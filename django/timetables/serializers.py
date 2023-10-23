"""
Implementação dos Serializers do app de timetables.

Contém os serializers para:
    - TimetableSerializer (Cronograma);
"""

import datetime

from rest_framework import serializers

from timetables.models import Timetable, Stage, StageExample
from activities.utils import check_worked_activity


class TimetableSerializer(serializers.ModelSerializer):
    """Serializer de Cronograma."""
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()

    class Meta:
        model = Timetable
        fields = '__all__'

    def get_start(self, obj):
        """Recupera a data de início."""
        queryset = obj.stages.all().order_by('start_date')

        if queryset.exists():
            return queryset.first().start_date.strftime("%d/%m/%Y")

        return None

    def get_end(self, obj):
        """Recupera a data de fim."""
        queryset = obj.stages.all().order_by('-send_date')

        if queryset.exists():
            return queryset.first().send_date.strftime("%d/%m/%Y")

        return None


class StageExampleSerializer(serializers.ModelSerializer):
    """Serializer de modelo de exemplo da etapa."""

    class Meta:
        model = StageExample
        fields = '__all__'


class StageSerializer(serializers.ModelSerializer):
    """Serializer de etapa do cronograma."""
    examples = StageExampleSerializer(many=True, read_only=True, source='stage_examples')
    activity_already_advanced = serializers.SerializerMethodField(read_only=True)
    past_stage = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Stage
        fields = [
            'id', 'description', 'start_date', 'send_date_supervisor', 'send_date', 'presentation_date',
            'activity_configuration', 'timetable', 'examples', 'activity_already_advanced', 'past_stage',
        ]

    def get_activity_already_advanced(self, obj):
        """Verifica se um etapa já foi adiantada."""
        if obj.activity_configuration is not None:
            return check_worked_activity(obj.activity_configuration)

        return False

    def get_past_stage(self, obj):
        """Verifica se a etapa é uma etapa passada."""
        today = datetime.date.today()

        if obj.start_date < today:
            return True

        if obj.send_date_supervisor < today:
            return True

        if obj.send_date < today:
            return True

        if obj.presentation_date is not None and obj.presentation_date < today:
            return True

        return False

    def validate_start_date(self, start_date):
        """Valida o campo de início."""
        today = datetime.date.today()

        if start_date < today:
            raise serializers.ValidationError('Não é possível manipular um etapa em que a data de início já passou.')

        return start_date

    def validate_send_date_supervisor(self, send_date_supervisor):
        """Valida o campo de data de envio ao orientador."""
        today = datetime.date.today()

        if send_date_supervisor < today:
            raise serializers.ValidationError('Não é possível manipular um etapa em que a data de envio ao orientador já passou.')

        return send_date_supervisor

    def validate_send_date(self, send_date):
        """Valida o campo de data de envio."""
        today = datetime.date.today()

        if send_date < today:
            raise serializers.ValidationError('Não é possível manipular um etapa em que a data de envio já passou.')

        return send_date

    def validate_presentation_date(self, presentation_date):
        """Valida o campo de data de apresentação."""
        today = datetime.date.today()

        if presentation_date is not None and presentation_date < today:
            raise serializers.ValidationError('Não é possível manipular um etapa em que a data de apresentação já passou.')

        return presentation_date

    def validate(self, attrs):
        """Valida todos os campos do serializer.

        A datas de envio ao supervisor, envio a plataforma
        deve ser após a data de início.

        A data de envio a plataforma deve ser antes da data de apresentação.

        A data de envio ao orientador deve ser antes da data de envio."""
        start_date = attrs.get('start_date')
        send_date_supervisor = attrs.get('send_date_supervisor')
        send_date = attrs.get('send_date')
        presentation_date = attrs.get('presentation_date')

        if start_date:
            if start_date > send_date_supervisor:
                raise serializers.ValidationError(
                    {'start_date': 'A data de envio ao supervisor deve ser após a data de início'}
                )

            if start_date > send_date:
                raise serializers.ValidationError(
                    {'start_date': 'A data de envio a plataforma deve ser após a data de início'}
                )

            if presentation_date is not None and start_date > presentation_date:
                raise serializers.ValidationError({
                    'start_date': 'A data de envio a plataforma deve ser após a data de início.',
                })

        if send_date_supervisor and send_date:
            if send_date_supervisor > send_date:
                raise serializers.ValidationError(
                    {'send_date_supervisor': 'A data de envio ao orientador deve ser antes da data de envio.'}
                )

        return attrs
