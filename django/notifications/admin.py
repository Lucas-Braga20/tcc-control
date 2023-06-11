"""
Admin configuration to notification app.
"""

from django.contrib import admin

from notifications.models import Notification, Receiver


@admin.register(Receiver)
class ReceiverAdmin(admin.ModelAdmin):
    """
    Receiver configuration model admin.
    """
    list_display = ('id', 'visualized', 'notification', 'user')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Notification configuration model admin.
    """
    list_display = ('id', 'description', 'author')
