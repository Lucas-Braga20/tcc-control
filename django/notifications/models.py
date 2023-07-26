"""
Notifications app models.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.datetime import get_datetime_tz


class Receiver(models.Model):
    """
    Receiver model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visualized = models.BooleanField(default=False, verbose_name=_('visualized'))
    notification = models.ForeignKey('notifications.Notification',
                                     verbose_name=_('notification'),
                                     related_name='notification',
                                     on_delete=models.CASCADE)
    user = models.ForeignKey('users.User',
                             verbose_name=_('user'),
                             related_name='notification',
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Receiver')
        verbose_name_plural = _('Receivers')

    def __str__(self):
        return f"Destinatário: {self.user} - Visualizado: {self.visualized}"


class Notification(models.Model):
    """
    Notification model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_('description'))
    author = models.ForeignKey('users.User', verbose_name=_('author'),
                               related_name='notification_author', on_delete=models.DO_NOTHING)
    receiver = models.ManyToManyField('users.User',
                                      related_name='notification_receiver',
                                      through='Receiver')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'), blank=False, null=True)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    def get_created_at(self):
        return get_datetime_tz(self.created_at).strftime("%d/%m/%Y %H:%M") if self.created_at is not None else None

    def __str__(self):
        return f"Notificação: {self.description}"
