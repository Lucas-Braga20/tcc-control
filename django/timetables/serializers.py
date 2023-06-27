"""
Timetable serializers.
"""

from rest_framework import serializers

from timetables.models import Timetable, Stage


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
        return obj.stages.all().order_by('start_date').first().start_date

    def get_end(self, obj):
        return obj.stages.all().order_by('-send_date').first().send_date


class StageSerializer(serializers.ModelSerializer):
    """
    Timetable stage Serializer.
    """

    class Meta:
        model = Stage
        fields = '__all__'
