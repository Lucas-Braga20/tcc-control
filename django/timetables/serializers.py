"""
Timetable serializers.
"""

import datetime

from rest_framework import serializers

from timetables.models import Timetable, Stage, StageExample
from activities.utils import check_worked_activity


class TimetableSerializer(serializers.ModelSerializer):
    """
    Timetable Serializer.
    """
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()

    class Meta:
        model = Timetable
        fields = '__all__'

    def get_start(self, obj):
        queryset = obj.stages.all().order_by('start_date')

        if queryset.exists():
            return queryset.first().start_date.strftime("%d/%m/%Y")

        return None

    def get_end(self, obj):
        queryset = obj.stages.all().order_by('-send_date')

        if queryset.exists():
            return queryset.first().send_date.strftime("%d/%m/%Y")

        return None


class StageExampleSerializer(serializers.ModelSerializer):
    """
    Stage example serializer.
    """

    class Meta:
        model = StageExample
        fields = '__all__'


class StageSerializer(serializers.ModelSerializer):
    """
    Timetable stage Serializer.
    """
    examples = StageExampleSerializer(many=True, read_only=True, source='stage_examples')
    activity_already_advanced = serializers.SerializerMethodField(read_only=True)
    past_stage = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Stage
        fields = ['id', 'description', 'start_date', 'send_date_supervisor', 'send_date',
                  'presentation_date', 'activity_configuration', 'timetable', 'examples',
                  'activity_already_advanced', 'past_stage']

    def get_activity_already_advanced(self, obj):
        if obj.activity_configuration is not None:
            return check_worked_activity(obj.activity_configuration)

        return False

    def get_past_stage(self, obj):
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
        today = datetime.date.today()

        if start_date < today:
            raise serializers.ValidationError('Não é possível manipular um etapa em que a data de início já passou.')

        return start_date

    def validate_send_date_supervisor(self, send_date_supervisor):
        today = datetime.date.today()

        if send_date_supervisor < today:
            raise serializers.ValidationError('Não é possível manipular um etapa em que a data de envio ao orientador já passou.')

        return send_date_supervisor

    def validate_send_date(self, send_date):
        today = datetime.date.today()

        if send_date < today:
            raise serializers.ValidationError('Não é possível manipular um etapa em que a data de envio já passou.')

        return send_date

    def validate_presentation_date(self, presentation_date):
        today = datetime.date.today()

        if presentation_date is not None and presentation_date < today:
            raise serializers.ValidationError('Não é possível manipular um etapa em que a data de apresentação já passou.')

        return presentation_date
