"""
Timetable app models.
"""

import uuid

from datetime import date

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
    archived = models.BooleanField(default=False, verbose_name=_('archived'))

    class Meta:
        verbose_name = _('Timetable')
        verbose_name_plural = _('Timetables')


class Stage(models.Model):
    """
    Timetable stage model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_('description'))
    start_date = models.DateField(verbose_name=_('start date'))
    send_date_supervisor = models.DateField(verbose_name=_('send date supervisor'))
    send_date = models.DateField(verbose_name=_('send date'))
    presentation_date = models.DateField(verbose_name=_('presentation date'),
                                         blank=True, null=True)
    activity_configuration = models.ForeignKey('activities.ActivityConfiguration',
                                               related_name='activity_configuration',
                                               verbose_name=_('activity configuration'),
                                               on_delete=models.DO_NOTHING)
    timetable = models.ForeignKey('timetables.TimeTable', related_name='stages',
                                  verbose_name=_('timetable'), on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = _('Stage')
        verbose_name_plural = _('Stages')

    def already_started(self):
        today = date.today()

        if today > self.start_date:
            return True

        if today > self.send_date_supervisor:
            return True

        if today > self.send_date:
            return True

        if self.presentation_date and today > self.presentation_date:
            return True

        return False


class StageExample(models.Model):
    """
    Stage example model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='documents/stage-example/', blank=True, null=True)
    stage = models.ForeignKey('timetables.Stage', related_name='stage_examples',
                              verbose_name=_('stage'), on_delete=models.CASCADE,
                              blank=True, null=True)

    class Meta:
        verbose_name = _('Stage example')
        verbose_name_plural = _('Stage examples')
