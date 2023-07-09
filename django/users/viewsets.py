"""
Users viewsets.
"""

from rest_framework import viewsets, mixins, permissions
from django_filters.rest_framework import DjangoFilterBackend

from users.models import User
from users.serializers import UserSerializer

from core.permissions import RoleAccessPermission


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
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
