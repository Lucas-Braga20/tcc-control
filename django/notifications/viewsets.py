"""
Implementação dos ViewSets do app de notifications.

Contém os endpoints para:
    - Notification (Notificação);
"""

from rest_framework import mixins, permissions, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from notifications.models import Notification, Receiver
from notifications.serializers import NotificationSerializer

from core.permissions import UserGroup

from notifications.utils import send_notification
from notifications.tasks import send_mail

from users.models import User


class NotificationViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """ViewSet para manipulação de notificação.

    Através deste endpoint que os usuários poderão criar ou
    recuperar as notificações.

    Métodos suportados:
        - Create;
        - Retrieve;
        - List;

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    model = Notification
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['description']

    def get_queryset(self):
        """Recupera o queryset de notificações."""
        no_page = self.request.query_params.get('no_page')
        if no_page:
            self.pagination_class = None

        user = self.request.user
        notifications = user.notification_receiver.all()
        queryset = notifications
        queryset = queryset.order_by('-created_at')

        visualized = self.request.query_params.get('visualized')
        if visualized:
            viewed = []
            not_viewed = []

            for notification in notifications:
                receiver_viewed = user.notification.filter(visualized=True, notification=notification)
                receiver_not_viewed = user.notification.filter(visualized=False, notification=notification)

                if receiver_viewed.exists():
                    viewed.append(receiver_viewed.first().notification.id)

                if receiver_not_viewed.exists():
                    not_viewed.append(receiver_not_viewed.first().notification.id)

            if visualized in (True, 'true'):
                queryset = notifications.filter(id__in=viewed).order_by('-created_at')

            if visualized in (False, 'false'):
                queryset = notifications.filter(id__in=not_viewed).order_by('-created_at')

        return queryset

    @action(detail=False, methods=['get'])
    def mark_all_read(self, request):
        """Ação de marcar como lida."""
        user = self.request.user

        receivers = Receiver.objects.filter(user=user, visualized=False)

        for receiver in receivers:
            receiver.visualized=True
            receiver.save()

        return Response(data={'success': True})

    @action(detail=False, methods=['post'], url_path='send-notification', url_name='send_notification')
    def send_notification(self, request):
        """Ação para enviar notificação de forma manual."""
        user = self.request.user

        user_group = UserGroup(user)

        if not user_group.is_teacher():
            return Response(data={
                'detail': 'Você não tem permissão para executar essa ação.',
            }, status=status.HTTP_403_FORBIDDEN)

        message = self.request.data.get('message')
        receivers = self.request.data.get('receivers')

        if not isinstance(message, str):
            return Response(data={
                'message': 'A mensagem deve ter um formato válido.',
            }, status=status.HTTP_400_BAD_REQUEST)

        if len(message) < 3:
            return Response(data={
                'message': 'A mensagem deve ter pelo menos 3 caracteres.',
            }, status=status.HTTP_400_BAD_REQUEST)

        if len(message) > 255:
            return Response(data={
                'message': 'A mensagem deve ter no máximo 255 caracteres.',
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            receivers = [User.objects.get(id=receiver) for receiver in receivers]
        except:
            return Response(data={
                'receivers': 'Insira destinatários válidos.',
            }, status=status.HTTP_400_BAD_REQUEST)

        description = f'O professor: "{user.get_full_name()}" enviou um aviso: {message}'

        send_notification(
            description=description,
            author=user,
            receivers=receivers,
        )

        send_mail.delay(
            description,
            'Aviso',
            [{
                'name': receiver.get_full_name(),
                'email': receiver.email,
            } for receiver in receivers],
        )

        return Response(data={
            'success': True,
        }, status=status.HTTP_200_OK)
