"""
Timetable serializers.
"""

from rest_framework import serializers

from timetables.models import Timetable, Step


class TimetableSerializer(serializers.ModelSerializer):
    """
    Timetable Serializer.
    """

    class Meta:
        model = Timetable
        fields = '__all__'


class StepSerializer(serializers.ModelSerializer):
    """
    Timetable Step Serializer.
    """

    class Meta:
        model = Step
        fields = '__all__'
