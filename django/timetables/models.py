"""
Timetable Models.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Timetable(models.Model):
    """
    Timetable model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_('description'))
    teacher = models.ForeignKey('users.User', related_name='teacher', verbose_name=_('teacher'),
                                on_delete=models.DO_NOTHING)
    participants = models.ManyToManyField('users.User', related_name='participants',
                                          verbose_name=_('pariticipants'))
