"""
Timetable serializers.
"""

from rest_framework import serializers

from timetables.models import Timetable, Stage, StageExample


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
            return queryset.first().start_date

        return None

    def get_end(self, obj):
        queryset = obj.stages.all().order_by('-send_date')

        if queryset.exists():
            return queryset.first().send_date

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

    class Meta:
        model = Stage
        fields = ['id', 'description', 'start_date', 'send_date_supervisor', 'send_date',
                  'presentation_date', 'activity_configuration', 'timetable', 'examples']
