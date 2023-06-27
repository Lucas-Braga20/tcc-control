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
        queryset = obj.stages.all().order_by('start_date')

        if queryset.exists():
            return queryset.first().start_date

        return None

    def get_end(self, obj):
        queryset = obj.stages.all().order_by('-send_date')

        if queryset.exists():
            return queryset.first().send_date

        return None


class StageSerializer(serializers.ModelSerializer):
    """
    Timetable stage Serializer.
    """

    class Meta:
        model = Stage
        fields = '__all__'
