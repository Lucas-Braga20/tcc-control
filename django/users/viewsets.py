"""
Users viewsets.
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
    """
    User viewset.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    model = User
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
    permission_classes = [permissions.IsAuthenticated, RoleAccessPermission]
    roles_required = ['Professor da disciplina']

    def get_queryset(self):
        queryset = super().get_queryset()

        if timetable := self.request.query_params.get('timetable'):
            queryset = queryset.filter(participants=timetable)

        if search := self.request.query_params.get('search'):
            queryset = queryset.annotate(
                full_name=Concat(F('first_name'), Value(' '), F('last_name'), output_field=CharField())
            ).filter(full_name__icontains=search)

        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_superuser:
            raise PermissionDenied('Não é possível alterar um admin.')

        return super().update(request, *args, **kwargs)
