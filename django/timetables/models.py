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


class Step(models.Model):
    """
    Timetable Setps model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_('description'))
    start_date = models.DateField(verbose_name=_('start date'))
    send_date_advisor = models.DateField(verbose_name=_('send date advisor'))
    send_date = models.DateField(verbose_name=_('send date'))
    presentation_date = models.DateField(verbose_name=_('presentation date'),
                                         blank=True, null=True)
    activity_configuration = models.ForeignKey('activities.ActivityConfiguration',
                                               related_name='activity_configuration',
                                               verbose_name=_('activity configuration'),
                                               on_delete=models.DO_NOTHING)


class StepExample(models.Model):
    """
    Step example model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='documents/step-example/', blank=True, null=True)
