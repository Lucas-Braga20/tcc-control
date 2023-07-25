"""
Viewsets to works app.
"""

from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from works.models import FinalWork, FinalWorkStage, FinalWorkVersion, ChangeRequest, VersionContentImage
from works.serializers import (
    FinalWorkSerializer, FinalWorkStageSerializer, FinalWorkVersionSerializer, ChangeRequestSerializer,
    VersionContentImageSerializer
)

from core.permissions import RoleAccessPermission, UserGroup
from core.defaults import WORK_STAGE_WAITING_CORRECTION, WORK_STAGE_ADJUSTED, WORK_STAGE_COMPLETED, completed_status

from notifications.serializers import NotificationSerializer


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

        queryset = queryset.filter(archived=False)

        return queryset


class FinalWorkStageViewSet(viewsets.ModelViewSet):
    """
    Final work stage viewset.
    """
    queryset = FinalWorkStage.objects.all()
    serializer_class = FinalWorkStageSerializer
    model = FinalWorkStage
    permission_classes = [RoleAccessPermission, permissions.IsAuthenticated]
    roles_required = ['Orientando', 'Professor da disciplina', 'Orientador']

    def get_queryset(self):
        queryset = super().get_queryset()

        user_group = UserGroup(self.request.user)

        if user_group.is_mentee():
            queryset = queryset.filter(final_work__mentees__in=[self.request.user])

        if user_group.is_supervisor():
            queryset = queryset.filter(final_work__supervisor=self.request.user)

        return queryset

    @action(detail=True, methods=['get'])
    def request_review(self, request, pk=None):
        object = self.get_object()

        user = self.request.user

        if not object.final_work.mentees.filter(id=user.id).exists():
            return Response(data={
                'work_stage': 'Você não pertence a este TCC.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if object.status in [4, 5, 6]:
            return Response(data={
                'status': 'Esta etapa já foi completada.'
            }, status=status.HTTP_400_BAD_REQUEST)

        object.status = WORK_STAGE_WAITING_CORRECTION
        object.save()

        receivers = []
        receivers.append(object.final_work.supervisor.id)

        notification_serializer = NotificationSerializer(data={
            'description': f'Os orientando(s) do TCC: "{object.final_work.description}" solicitaram uma correção na ' \
                           f'etapa: {object.stage.description}',
            'author': user.id,
            'receiver': receivers,
        })

        notification_serializer.is_valid(raise_exception=True)
        notification_serializer.save()

        headers = self.get_success_headers(notification_serializer.data)
        return Response(notification_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def mark_reviewed(self, request, pk=None):
        object = self.get_object()

        user = self.request.user

        if object.final_work.supervisor.id != user.id:
            return Response(data={
                'work_stage': 'Você não pertence a este TCC.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if object.status in [4, 5, 6]:
            return Response(data={
                'status': 'Esta etapa já foi completada.'
            }, status=status.HTTP_400_BAD_REQUEST)

        object.status = WORK_STAGE_ADJUSTED
        object.save()

        receivers = list(object.final_work.mentees.values_list('id', flat=True))

        notification_serializer = NotificationSerializer(data={
            'description': f'O supervisor do TCC: "{object.final_work.description}" marcou como corrigido a etapa: ' \
                           f'{object.stage.description}',
            'author': user.id,
            'receiver': receivers,
        })

        notification_serializer.is_valid(raise_exception=True)
        notification_serializer.save()

        headers = self.get_success_headers(notification_serializer.data)
        return Response(notification_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def mark_completed(self, request, pk=None):
        object = self.get_object()

        user = self.request.user

        if UserGroup(user).is_teacher() is False:
            return Response(data={
                'work_stage': 'Você não é professor.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if object.status in completed_status:
            return Response(data={
                'status': 'Esta etapa já foi completada.'
            }, status=status.HTTP_400_BAD_REQUEST)

        object.status = WORK_STAGE_COMPLETED
        object.save()

        receivers = list(object.final_work.mentees.values_list('id', flat=True))

        notification_serializer = NotificationSerializer(data={
            'description': f'O professor: "{user.get_full_name()}" marcou como concluído a etapa: ' \
                           f'{object.stage.description}',
            'author': user.id,
            'receiver': receivers,
        })

        notification_serializer.is_valid(raise_exception=True)
        notification_serializer.save()

        headers = self.get_success_headers(notification_serializer.data)
        return Response(notification_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FinalWorkVersionViewSet(viewsets.ModelViewSet):
    """
    Final work version viewset.
    """
    queryset = FinalWorkVersion.objects.all()
    serializer_class = FinalWorkVersionSerializer
    model = FinalWorkVersion
    permission_classes = [RoleAccessPermission, permissions.IsAuthenticated]
    roles_required = ['Orientando', 'Professor da disciplina', 'Orientador']

    def get_queryset(self):
        queryset = super().get_queryset()

        user_group = UserGroup(self.request.user)

        if user_group.is_mentee():
            queryset = queryset.filter(work_stage__final_work__mentees__in=[self.request.user])

        if user_group.is_supervisor():
            queryset = queryset.filter(work_stage__final_work__supervisor=self.request.user)

        return queryset


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
    permission_classes = [RoleAccessPermission, permissions.IsAuthenticated]
    roles_required = ['Orientando', 'Professor da disciplina', 'Orientador']

    def get_queryset(self):
        queryset = super().get_queryset()

        user_group = UserGroup(self.request.user)

        if user_group.is_mentee():
            queryset = queryset.filter(version__work_stage__final_work__mentees__in=[self.request.user])

        if user_group.is_supervisor():
            queryset = queryset.filter(version__work_stage__final_work__supervisor=self.request.user)

        return queryset


class ChangeRequestViewSet(viewsets.ModelViewSet):
    """
    Change request viewset.
    """
    queryset = ChangeRequest.objects.all()
    serializer_class = ChangeRequestSerializer
    model = ChangeRequest
    permission_classes = [RoleAccessPermission, permissions.IsAuthenticated]
    roles_required = ['Orientando', 'Professor da disciplina']
