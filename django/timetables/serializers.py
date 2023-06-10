"""
Timetable serializers.
"""

from rest_framework import serializers

from timetables.models import Timetable


class TimetableSerializer(serializers.ModelSerializer):
    """
    Timetable Serializer.
    """

    class Meta:
        """
        Class meta to time table serializer.
        """
        model = Timetable
        fields = '__all__'
