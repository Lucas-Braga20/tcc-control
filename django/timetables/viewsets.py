"""
Timetable viewsets.
"""

from rest_framework import viewsets

from timetables.models import Timetable
from timetables.serializers import TimetableSerializer


class TimetableViewSet(viewsets.ModelViewSet):
    """
    Timtable viewset provides all http request methods.
    """
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    model = Timetable
