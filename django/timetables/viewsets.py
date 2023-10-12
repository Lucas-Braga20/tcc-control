"""
Implementação dos ViewSets do app de timetables.

Contém os endpoints para:
    - Timetables (Cronogramas);
    - Stage (Etapas);
"""

import os
import datetime

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, mixins, status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from core.mixins import DisablePaginationMixin
from core.permissions import RoleAccessPermission

from activities.utils import check_worked_activity
from activities.models import ActivityConfiguration

from timetables.models import Timetable, Stage, StageExample
from timetables.serializers import TimetableSerializer, StageSerializer


class TimetableViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet para manipulação de cronogramas.

    Através deste endpoint que o professor da disciplina poderá ver
    todas os seus cronogramas.

    Métodos suportados:
        - Retrieve;
        - List;
        - Update;

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;
    """
    model = Timetable
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['archived']
    permission_classes = [permissions.IsAuthenticated, RoleAccessPermission]
    roles_required = ['Professor da disciplina']

    def get_queryset(self):
        """Recupera o queryset de cronoramas."""
        queryset = super().get_queryset()

        queryset = queryset.filter(teacher=self.request.user)

        return queryset

    def update(self, request, *args, **kwargs):
        """Atualização de cronograma."""
        instance = self.get_object()
        stages = instance.stages.all()

        data = request.data
        archived = data.get('archived')

        if archived == True:
            for stage in stages:
                if stage.already_started():
                    return Response(data={
                        'detail': 'Cannot archive a schedule that has already started.',
                    }, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)


class StageViewSet(DisablePaginationMixin, viewsets.ModelViewSet):
    """ViewSet para manipulação de etapas.

    Através deste endpoint que o professor da disciplina poderá ver,
    criar, atualizar e deletar todas as etapas que relacionadas
    ao seu cronograma.

    Métodos suportados:
        - Retrieve;
        - List;
        - Create;
        - Update;
        - Delete;

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;
    """
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['timetable']
    ordering_fields = ['start_date']
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [permissions.IsAuthenticated, RoleAccessPermission]
    roles_required = ['Professor da disciplina', 'Orientador', 'Orientando']

    def get_queryset(self):
        """Recupera o queryset de etapas."""
        queryset = super().get_queryset()

        queryset = queryset.filter(timetable__teacher=self.request.user)

        no_page = self.request.query_params.get('no_page')
        if no_page:
            self.pagination_class = None

        return queryset

    def create(self, request, *args, **kwargs):
        """Cria uma nova etapa."""
        body = self.request.data.copy()

        serializer = self.get_serializer(data=body)
        serializer.is_valid(raise_exception=True)

        files = request.FILES.getlist('examples')
        for file in files:
            extension = os.path.splitext(file.name)[1]
            if extension.lower() not in ['.pdf', '.docx', '.doc']:
                return Response(
                    data={'examples': 'Apenas PDF ou DOC/DOCX são permitidos.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

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
        """Atualiza uma etapa."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data

        today = datetime.date.today()
        
        if instance.start_date < today:
            return Response(
                data={'detail': 'Não é possível alterar uma etapa passada.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        activity_configuration_id = data.get('activity_configuration')

        if activity_configuration_id is not None and instance.activity_configuration is not None:
            activity_configuration = ActivityConfiguration.objects.filter(id=activity_configuration_id)

            if not activity_configuration.exists():
                return Response(
                    data={'activity_configuration': 'Esta configuração de atividade não existe.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            activity_configuration = activity_configuration.first()

            if activity_configuration != instance.activity_configuration:
                already_advanced = check_worked_activity(instance.activity_configuration)

                if already_advanced:
                    stages = instance.work_timetable_stage.all()

                    for work_stage in stages:
                        last_version = work_stage.get_last_version()

                        if last_version:
                            activity_fields = activity_configuration.fields
                            content = []

                            for fields in activity_fields['fields']:
                                content.append({
                                    'key': fields['key'],
                                    'value': '',
                                })

                            last_version.content = {
                                'fields': content
                            }
                            last_version.save()

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)

        files = request.FILES.getlist('examples')
        for file in files:
            extension = os.path.splitext(file.name)[1]
            if extension.lower() not in ['.pdf', '.docx', '.doc']:
                return Response(
                    data={'examples': 'Apenas PDF ou DOC/DOCX são permitidos.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

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

    def destroy(self, request, *args, **kwargs):
        """Deleta uma etapa."""
        instance = self.get_object()

        if instance.already_started():
            return Response(
                data={'detail': 'Cannot remove a step that has already started'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
