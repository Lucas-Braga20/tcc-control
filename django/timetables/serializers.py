"""
Timetable serializers.
"""

from rest_framework import serializers

from timetables.models import Timetable, Stage


class TimetableSerializer(serializers.ModelSerializer):
    """
    Timetable Serializer.
    """

    class Meta:
        model = Timetable
        fields = '__all__'


class StageSerializer(serializers.ModelSerializer):
    """
    Timetable stage Serializer.
    """

    class Meta:
        model = Stage
        fields = '__all__'
