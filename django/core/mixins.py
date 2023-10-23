"""Mixins para o app core.

Contém os mixins:
    - DisablePaginationMixin;
    - NotificationMixin;
"""

from rest_framework.response import Response


class DisablePaginationMixin:
    """Mixin de controle de paginação."""

    def paginate_queryset(self, queryset):
        """Implementa a paginação no queryset."""

        if 'pagination' in self.request.query_params:
            pagination_enabled = self.request.query_params.get('pagination').lower() == 'true'
            if not pagination_enabled:
                return None

        return super().paginate_queryset(queryset)

    def get_paginated_response(self, data):
        """Recupera o response em páginas."""
        if data is None:
            return Response(data)

        return super().get_paginated_response(data)


class NotificationMixin:
    """Mixin de notificação.

    Insere no contexto de toda view com esse mixin
    os valores de notificação.
    """

    def get_context_data(self, **kwargs):
        """Gera o contexto do template."""
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if user:
            notifications = user.notification_receiver.all().order_by('-created_at')

            viewed = []
            not_viewed = []

            for notification in notifications:
                receiver_viewed = user.notification.filter(visualized=True, notification=notification)
                receiver_not_viewed = user.notification.filter(visualized=False, notification=notification)

                if receiver_viewed.exists():
                    viewed.append(receiver_viewed.first().notification.id)

                if receiver_not_viewed.exists():
                    not_viewed.append(receiver_not_viewed.first().notification.id)

            context['notifications'] = {
                'all': notifications,
                'viewed': notifications.filter(id__in=viewed),
                'not_viewed': notifications.filter(id__in=not_viewed),
                'count': notifications.count(),
            }
        else:
            context['notifications'] = None

        return context
