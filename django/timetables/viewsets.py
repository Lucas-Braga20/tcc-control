"""
Timetable viewsets.
"""

from rest_framework import viewsets

from timetables.models import Timetable, Step
from timetables.serializers import TimetableSerializer, StepSerializer


class TimetableViewSet(viewsets.ModelViewSet):
    """
    Timtable viewset provides all http request methods.
    """
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    model = Timetable


class StepViewSet(viewsets.ModelViewSet):
    """
    Timetable step viewset provides all http request methods.
    """
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    model = Step
