"""
Notifications Models.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Receiver(models.Model):
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


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_('description'))
    author = models.ForeignKey('users.User', verbose_name=_('author'),
                               related_name='notification_author', on_delete=models.DO_NOTHING)
    receiver = models.ManyToManyField('users.User',
                                      related_name='notification_receiver',
                                      through='Receiver')
