"""
Implementação dos ViewSets do app de activities.

Contém os endpoints para:
    - Timetables (Cronogramas);
    - Stage (Etapas);
"""

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from core.permissions import RoleAccessPermission

from activities.models import ActivityConfiguration
from activities.serializers import ActivityConfigurationSerializer


class ActivityConfigurationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet para manipulação de configurações de atividade.

    Através deste endpoint que o professor da disciplina poderá ver
    ou atualizar as atividades.

    Métodos suportados:
        - Retrieve;
        - List;
        - Update;

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;
    """
    model = ActivityConfiguration
    queryset = ActivityConfiguration.objects.all()
    serializer_class = ActivityConfigurationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['archived']
    search_fields = ['name']
    permission_classes = [permissions.IsAuthenticated, RoleAccessPermission]
    roles_required = ['Professor da disciplina']

    def get_queryset(self):
        """Recupera o queryset de atividades."""
        queryset = super().get_queryset()

        no_page = self.request.query_params.get('no_page')
        if no_page:
            self.pagination_class = None

        return queryset

    def update(self, request, *args, **kwargs):
        """Atualização de atividade."""
        instance = self.get_object()

        if instance.archived is True:
            if 'archived' in request.data and request.data['archived'] is False:
                instance.archived = False
                instance.save()
                serializer = self.get_serializer(instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    data={'detail': 'You can only change an activity setting if it is not archived'},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED,
                )

        return super().update(request, *args, **kwargs)
