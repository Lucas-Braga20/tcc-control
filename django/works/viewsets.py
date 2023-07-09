"""
Viewsets to works app.
"""

from rest_framework import viewsets, mixins, permissions

from works.models import FinalWork, FinalWorkStage, FinalWorkVersion, ChangeRequest, VersionContentImage
from works.serializers import (
    FinalWorkSerializer, FinalWorkStageSerializer, FinalWorkVersionSerializer, ChangeRequestSerializer,
    VersionContentImageSerializer
)

from core.permissions import RoleAccessPermission, UserGroup


class FinalWorkViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """
    Final work viewset.
    """
    queryset = FinalWork.objects.all()
    serializer_class = FinalWorkSerializer
    model = FinalWork
    permission_classes = [RoleAccessPermission, permissions.IsAuthenticated]
    roles_required = ['Orientando', 'Professor da disciplina', 'Orientador']

    def get_permissions(self):
        if self.action == 'update':
            self.role_required = ['Professor da disciplina']
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()

        user_group = UserGroup(self.request.user)

        if user_group.is_mentee():
            queryset = queryset.filter(mentees__in=[self.request.user])

        if user_group.is_supervisor():
            queryset = queryset.filter(supervisor=self.request.user)

        return queryset


class FinalWorkStageViewSet(viewsets.ModelViewSet):
    """
    Final work stage viewset.
    """
    queryset = FinalWorkStage.objects.all()
    serializer_class = FinalWorkStageSerializer
    model = FinalWorkStage


class FinalWorkVersionViewSet(viewsets.ModelViewSet):
    """
    Final work version viewset.
    """
    queryset = FinalWorkVersion.objects.all()
    serializer_class = FinalWorkVersionSerializer
    model = FinalWorkVersion


class VersionContentImageViewSet(mixins.CreateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin,
                                 mixins.ListModelMixin,
                                 viewsets.GenericViewSet):
    """
    Version content image viewset.
    """
    queryset = VersionContentImage.objects.all()
    serializer_class = VersionContentImageSerializer
    model = VersionContentImage
    authentication_classes = []
    permission_classes = []


class ChangeRequestViewSet(viewsets.ModelViewSet):
    """
    Change request viewset.
    """
    queryset = ChangeRequest.objects.all()
    serializer_class = ChangeRequestSerializer
    model = ChangeRequest
