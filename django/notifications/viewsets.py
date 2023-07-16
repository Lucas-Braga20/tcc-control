"""
Notification viewsets.
"""

from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from notifications.models import Notification, Receiver
from notifications.serializers import NotificationSerializer

from django_filters.rest_framework import DjangoFilterBackend


class NotificationViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    """
    Notification viewset.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    model = Notification
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['description']

    def get_queryset(self):
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
        user = self.request.user

        receivers = Receiver.objects.filter(user=user, visualized=False)

        for receiver in receivers:
            receiver.visualized=True
            receiver.save()

        return Response(data={'success': True})
