"""
Configurações de Adminsitração do app de notifications.

Contém as configurações para:
    - ReceiverAdmin;
    - NotificationAdmin;
"""

from django.contrib import admin

from notifications.models import Notification, Receiver


@admin.register(Receiver)
class ReceiverAdmin(admin.ModelAdmin):
    """Configuração de administração para o Receiver modelo."""
    list_display = ('id', 'visualized', 'notification', 'user')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Configuração de administração para o Notification modelo."""
    list_display = ('id', 'description', 'author')
