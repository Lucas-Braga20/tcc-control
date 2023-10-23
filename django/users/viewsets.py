"""
Implementação dos ViewSets do app de users.

Contém os endpoints para:
    - UserViewSet (Usuários);
"""

from rest_framework import viewsets, mixins, permissions
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import F, Value, CharField
from django.db.models.functions import Concat

from users.models import User
from users.serializers import UserSerializer

from core.permissions import RoleAccessPermission


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet para manipulação de usuários.

    Através deste endpoint que o professor da disciplina poderá ver
    e atualizar os usuários

    Métodos suportados:
        - Retrieve;
        - List;
        - Update;

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    model = User
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
    permission_classes = [permissions.IsAuthenticated, RoleAccessPermission]
    roles_required = ['Professor da disciplina']

    def get_queryset(self):
        """Recupera o queryset de usuários."""
        queryset = super().get_queryset()

        if timetable := self.request.query_params.get('timetable'):
            queryset = queryset.filter(participants=timetable)

        if search := self.request.query_params.get('search'):
            queryset = queryset.annotate(
                full_name=Concat(F('first_name'), Value(' '), F('last_name'), output_field=CharField())
            ).filter(full_name__icontains=search)

        return queryset

    def update(self, request, *args, **kwargs):
        """Atualiza um usuário."""
        instance = self.get_object()

        if instance.is_superuser:
            raise PermissionDenied('Não é possível alterar um admin.')

        return super().update(request, *args, **kwargs)
