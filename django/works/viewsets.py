"""
Viewsets to works app.
"""

import datetime

from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from works.models import FinalWork, FinalWorkStage, FinalWorkVersion, ChangeRequest, VersionContentImage
from works.utils import get_document_creation_time
from works.serializers import (
    FinalWorkSerializer, FinalWorkStageSerializer, FinalWorkVersionSerializer, ChangeRequestSerializer,
    VersionContentImageSerializer
)

from users.models import User
from users.serializers import UserSerializer

from core.permissions import RoleAccessPermission, UserGroup
from core.utils import generate_work_stages
from core.defaults import (
    WORK_STAGE_WAITING_CORRECTION, WORK_STAGE_ADJUSTED, WORK_STAGE_COMPLETED, WORK_STAGE_PRESENTED,
    WORK_STAGE_COMPLETED_LATE, WORK_STAGE_UNDER_CHANGE, WORK_STAGE_UPDATED, completed_status
)

from notifications.utils import send_notification
from notifications.tasks import send_mail

from timetables.models import Timetable


class FinalWorkViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Final work viewset.
    """
    queryset = FinalWork.objects.all()
    serializer_class = FinalWorkSerializer
    model = FinalWork
    permission_classes = [RoleAccessPermission, permissions.IsAuthenticated]
    roles_required = ['Orientando', 'Professor da disciplina', 'Orientador']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['completed']

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

    def update(self, request, *args, **kwargs):
        data = request.data
        approved = data.get('approved')
        completed = data.get('completed')
        able_to_present = data.get('able_to_present')

        final_work = self.get_object()

        if approved and approved is True:
            # today = datetime.date.today()
            # today hard coded
            today = datetime.date(2023, 3, 4)

            timetable = Timetable.objects.filter(stages__start_date__lte=today,
                                                 stages__send_date__gte=today,
                                                 archived=False).first()

            generate_work_stages(final_work=final_work, timetable=timetable)

        if completed and completed is True:
            final_work.completed = True
            final_work.save()

        if able_to_present:
            if able_to_present is None:
                final_work.able_to_present = None
                final_work.save()
            elif able_to_present is True:
                final_work.able_to_present = True
                final_work.save()
            elif able_to_present is False:
                final_work.able_to_present = False
                final_work.save()

        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['get'], url_path='available-supervisors')
    def available_supervisors(self, request, pk=None):
        supervisors = User.objects.filter(groups__name='orientador', is_active=True)

        users = UserSerializer(data=supervisors, many=True)
        users.is_valid()

        return Response(users.data)

    @action(detail=True, methods=['get'], url_path='available-mentees')
    def available_mentees(self, request, pk=None):
        instance = self.get_object()
        mentees = User.objects.filter(groups__name='orientando', is_active=True)
        mentees = list(filter(lambda mentee: (mentee.get_already_in_work() is False), mentees))
        mentees = mentees + list(instance.mentees.all())

        users = UserSerializer(data=mentees, many=True)
        users.is_valid()

        return Response(users.data)

    @action(detail=True, methods=['get'], url_path='documents')
    def get_documents(self, request, pk=None):
        instance = self.get_object()

        documents = instance.get_final_documents()

        documents = [{
            'path': document,
            'creation_time': get_document_creation_time(document),
        } for document in documents]

        documents = list(sorted(
            documents,
            key=lambda final_document: final_document['creation_time'],
            reverse=True,
        ))

        documents = [{
            'path': document.get('path'),
            'creation_time': document.get('creation_time').strftime('%d-%m-%Y %H:%M:%S'),
        } for document in documents]

        return Response({
            'documents': documents,
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='generate-document')
    def generate_document(self, request, pk=None):
        instance = self.get_object()

        response = instance.generate_final_document()

        if response is None:
            return Response(data={
                'detail': 'Houve um erro ao gerar o documento.',
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={
            'document': {
                'path': response,
                'creation_time': get_document_creation_time(response, concat=False),
            },
        }, status=status.HTTP_200_OK)


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
        self.object = self.get_object()

        user = self.request.user

        if not self.object.final_work.mentees.filter(id=user.id).exists():
            return Response(data={
                'work_stage': 'Você não pertence a este TCC.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if self.object.status in [4, 5, 6]:
            return Response(data={
                'status': 'Esta etapa já foi completada.'
            }, status=status.HTTP_400_BAD_REQUEST)

        self.object.status = WORK_STAGE_WAITING_CORRECTION
        self.object.save()

        receivers = []
        receivers.append(self.object.final_work.supervisor)

        description = (
            f'Os orientando(s) do TCC: "{self.object.final_work.description}" solicitaram uma ' \
            f'correção na etapa: {self.object.stage.description}'
        )

        notification = send_notification(
            description=description,
            author=user,
            receivers=receivers,
        )

        send_mail.delay(
            description,
            'Solicitação de correção',
            [{
                'name': receiver.get_full_name(),
                'email': receiver.email,
            } for receiver in receivers],
        )

        headers = self.get_success_headers(notification.data)
        return Response(notification.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def mark_reviewed(self, request, pk=None):
        self.object = self.get_object()

        user = self.request.user

        if self.object.final_work.supervisor.id != user.id:
            return Response(data={
                'work_stage': 'Você não pertence a este TCC.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if self.object.status in [4, 5, 6]:
            return Response(data={
                'status': 'Esta etapa já foi completada.'
            }, status=status.HTTP_400_BAD_REQUEST)

        self.object.status = WORK_STAGE_ADJUSTED
        self.object.save()

        receivers = list(self.object.final_work.mentees.all())

        description = (
            f'O supervisor do TCC: "{self.object.final_work.description}" marcou como corrigido a ' \
            f'etapa: "{self.object.stage.description}"'
        )

        notification = send_notification(
            description=description,
            author=user,
            receivers=receivers,
        )

        send_mail.delay(
            description,
            'Correção',
            [{
                'name': receiver.get_full_name(),
                'email': receiver.email,
            } for receiver in receivers],
        )

        headers = self.get_success_headers(notification.data)
        return Response(notification.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def mark_completed(self, request, pk=None):
        self.object = self.get_object()

        user = self.request.user

        if UserGroup(user).is_teacher() is False and UserGroup(user).is_mentee() is False:
            return Response(data={
                'work_stage': 'Você não é professor ou orientando.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if self.object.status in completed_status:
            return Response(data={
                'status': 'Esta etapa já foi completada.'
            }, status=status.HTTP_400_BAD_REQUEST)

        today = datetime.date.today()

        if today > self.object.stage.send_date:
            self.object.status = WORK_STAGE_COMPLETED_LATE
        else:
            self.object.status = WORK_STAGE_COMPLETED

        self.object.save()

        receivers = list(self.object.final_work.mentees.all())

        group_name = 'professor'

        if UserGroup(user).is_mentee():
            group_name = 'orientando'

        description = (
            f'O {group_name}: "{user.get_full_name()}" marcou como concluído a etapa: ' \
            f'{self.object.stage.description}'
        )

        notification = send_notification(
            description=description,
            author=user,
            receivers=receivers
        )

        send_mail.delay(
            description,
            'Conclusão de etapa',
            [{
                'name': receiver.get_full_name(),
                'email': receiver.email,
            } for receiver in receivers],
        )

        headers = self.get_success_headers(notification.data)
        return Response(notification.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def mark_presented(self, request, pk=None):
        self.object = self.get_object()

        user = self.request.user

        if UserGroup(user).is_teacher() is False:
            return Response(data={
                'work_stage': 'Você não é professor.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if self.object.status in [WORK_STAGE_PRESENTED]:
            return Response(data={
                'status': 'Esta etapa já foi apresentada.'
            }, status=status.HTTP_400_BAD_REQUEST)

        self.object.status = WORK_STAGE_PRESENTED
        self.object.save()

        receivers = list(self.object.final_work.mentees.all())

        description = (
            f'O professor: "{user.get_full_name()}" marcou como apresentado a etapa: ' \
            f'{self.object.stage.description}'
        )

        notification = send_notification(
            description=description,
            author=user,
            receivers=receivers
        )

        send_mail.delay(
            description,
            'Apresentação',
            [{
                'name': receiver.get_full_name(),
                'email': receiver.email,
            } for receiver in receivers],
        )

        headers = self.get_success_headers(notification.data)
        return Response(notification.data, status=status.HTTP_201_CREATED, headers=headers)


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        user = self.request.user

        description = (
            f'O orientando do TCC: "{serializer.instance.work_stage.final_work.description}" ' \
            f'solicitou uma alteração na etapa: {serializer.instance.work_stage.stage.description}'
        )

        receivers = [serializer.instance.work_stage.stage.timetable.teacher]

        send_notification(
            description=description,
            author=user,
            receivers=receivers,
        )

        send_mail.delay(
            description,
            'Alteração',
            [{
                'name': receiver.get_full_name(),
                'email': receiver.email,
            } for receiver in receivers],
        )

        last_version = instance.work_stage.get_last_version()

        activity_fields = instance.work_stage.stage.activity_configuration.fields
        content = []

        for fields in activity_fields['fields']:
            content.append({
                'key': fields['key'],
                'value': '',
            })

        if last_version:
            version = FinalWorkVersion(
                content=instance.work_stage.get_last_version().content,
                work_stage=instance.work_stage
            )
        else:
            version = FinalWorkVersion(
                content={
                    'fields': content,
                },
                work_stage=instance.work_stage
            )

        instance.work_stage.status = WORK_STAGE_UNDER_CHANGE
        instance.work_stage.save()

        version.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        user = self.request.user

        if serializer.instance.approved:
            message = 'aprovou'
        else:
            message = 'reprovou'

        description = (
            f'O professor: "{user.get_full_name()}" {message} a solicitação de alteração da etapa: ' \
            f'{serializer.instance.work_stage.stage.description}'
        )

        receivers = list(serializer.instance.work_stage.final_work.mentees.all())

        send_notification(
            description=description,
            author=user,
            receivers=receivers,
        )

        send_mail.delay(
            description,
            'Solicitação de alteração',
            [{
                'name': receiver.get_full_name(),
                'email': receiver.email,
            } for receiver in receivers],
        )

        if serializer.instance.approved:
            serializer.instance.work_stage.status = WORK_STAGE_UPDATED
            serializer.instance.work_stage.save()

            version = serializer.instance.work_stage.get_last_version()

            if version.confirmed == False:
                version.confirmed = True
                version.save()
        else:
            serializer.instance.work_stage.status = WORK_STAGE_COMPLETED
            serializer.instance.work_stage.save()

            version = serializer.instance.work_stage.get_last_version()

            if version.confirmed == False:
                version.delete()

        return Response(serializer.data)
