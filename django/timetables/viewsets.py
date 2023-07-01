"""
Timetable viewsets.
"""

from rest_framework import viewsets, mixins

from timetables.models import Timetable, Stage
from timetables.serializers import TimetableSerializer, StageSerializer

from django_filters.rest_framework import DjangoFilterBackend


class TimetableViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    """
    Timtable viewset.
    """
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    model = Timetable
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['archived']
    permission_classes = []
    authentication_classes = []


class StageViewSet(viewsets.ModelViewSet):
    """
    Timetable stage.
    """
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    model = Stage
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['timetable']
    permission_classes = []
    authentication_classes = []

    def get_queryset(self):
        queryset = super().get_queryset()

        no_page = self.request.query_params.get('no_page')
        if no_page:
            self.pagination_class = None

        return queryset
