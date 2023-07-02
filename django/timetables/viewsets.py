"""
Timetable viewsets.
"""

import os

from rest_framework import viewsets, mixins, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from timetables.models import Timetable, Stage, StageExample
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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['timetable']
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = []
    authentication_classes = []

    def get_queryset(self):
        queryset = super().get_queryset()

        no_page = self.request.query_params.get('no_page')
        if no_page:
            self.pagination_class = None

        return queryset

    def create(self, request, *args, **kwargs):
        body = self.request.data.copy()

        serializer = self.get_serializer(data=body)
        serializer.is_valid(raise_exception=True)

        files = request.FILES.getlist('examples')
        for file in files:
            extension = os.path.splitext(file.name)[1]
            if extension.lower() not in ['.pdf', '.docx']:
                return Response(data={'examples': 'Only PDF or DOCX files are allowed.'},
                                status=status.HTTP_400_BAD_REQUEST)

        stage = serializer.save()

        for file in files:
            stage_example = StageExample.objects.create(
                stage=stage,
                file=file,
            )
            stage_example.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        files = request.FILES.getlist('examples')
        for file in files:
            extension = os.path.splitext(file.name)[1]
            if extension.lower() not in ['.pdf', '.docx']:
                return Response(data={'examples': 'Only PDF or DOCX files are allowed.'},
                                status=status.HTTP_400_BAD_REQUEST)

        stage = serializer.save()

        already_uploaded = request.data.getlist('already_uploaded', [])
        stage.stage_examples.all().exclude(id__in=already_uploaded).delete()

        for file in files:
            stage_example = StageExample.objects.create(
                stage=stage,
                file=file,
            )
            stage_example.save()

        return Response(serializer.data)
