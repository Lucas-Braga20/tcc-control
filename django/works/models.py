"""
Works app models.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core import defaults


class FinalWork(models.Model):
    """
    Final work model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_('description'))
    approved = models.BooleanField(verbose_name=_('approved'), default=False)
    supervisor = models.ForeignKey('users.User', related_name='work_supervisor', verbose_name=_('supervisor'),
                                   on_delete=models.DO_NOTHING)
    mentees = models.ManyToManyField('users.User', related_name='work_mentee',
                                    verbose_name=_('mentee'))

    class Meta:
        verbose_name = _('Final work')
        verbose_name_plural = _('Final works')


class FinalWorkStage(models.Model):
    """
    Final work stage model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    presented = models.BooleanField(verbose_name=_('presented'), default=False)
    status = models.IntegerField(verbose_name=_('status'),
                                 choices=defaults.WORK_STAGE_STATUS,
                                 default=defaults.WORK_STAGE_ASSIGNED)
    stage = models.ForeignKey('timetables.Stage', verbose_name=_('time table stage'),
                              on_delete=models.DO_NOTHING, related_name='work_timetable_stage')
    final_work = models.ForeignKey('works.FinalWork', verbose_name=_('final work'),
                                   on_delete=models.DO_NOTHING, related_name='work_stage')

    class Meta:
        verbose_name = _('Final work stage')
        verbose_name_plural = _('Final work stages')


class FinalWorkVersion(models.Model):
    """
    Final work version model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('created at'))
    content = models.JSONField(verbose_name=_('content'), blank=True, null=True)
    work_stage = models.ForeignKey('works.FinalWorkStage', verbose_name=_('work stage'),
                                   on_delete=models.DO_NOTHING, related_name='work_stage_version')

    class Meta:
        verbose_name = _('Work stage version')
        verbose_name_plural = _('Work stage versions')


class ChangeRequest(models.Model):
    """
    Change request model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    approved = models.BooleanField(verbose_name=_('approved'), default=False)
    description = models.TextField(verbose_name=_('description'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('created at'))
    requester = models.ForeignKey('users.User', verbose_name=_('requester'),
                                  on_delete=models.DO_NOTHING, related_name='requester')
    work_stage = models.ForeignKey('works.FinalWorkStage', verbose_name=_('work stage'),
                                   on_delete=models.DO_NOTHING, related_name='work_stage_change_request')

    class Meta:
        verbose_name = _('Change request')
        verbose_name_plural = _('Change requests')

    def approve_request(self):
        """
        Method to approve a change request.
        """
        self.approved = True
        new_version = FinalWorkVersion(content=None, work_stage=self.work_stage)
        self.save()
        new_version.save()
