"""
Timetable viewsets.
"""

from rest_framework import viewsets, mixins

from timetables.models import Timetable, Stage
from timetables.serializers import TimetableSerializer, StageSerializer


class TimetableViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Timtable viewset.
    """
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    model = Timetable


class StageViewSet(viewsets.ModelViewSet):
    """
    Timetable stage.
    """
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    model = Stage
