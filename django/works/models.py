"""
Works app models.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core import defaults


class TCCWork(models.Model):
    """
    TCC work model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_('description'))
    approved = models.BooleanField(verbose_name=_('approved'), default=False)
    advisor = models.ForeignKey('users.User', related_name='advisor', verbose_name=_('advisor'),
                                on_delete=models.DO_NOTHING)
    advised = models.ManyToManyField('users.User', related_name='advised',
                                     verbose_name=_('advised'))

    class Meta:
        verbose_name = _('TCC work')
        verbose_name_plural = _('TCC works')


class WorkStep(models.Model):
    """
    Work step model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    presented = models.BooleanField(verbose_name=_('presented'), default=False)
    status = models.SmallIntegerField(verbose_name=_('status'),
                                      choices=defaults.WORK_STEP_STATUS,
                                      default=defaults.WORK_STEP_ASSIGNED)
    step = models.ForeignKey('timetables.Step', verbose_name=_('step'),
                             on_delete=models.DO_NOTHING, related_name='step')
    tcc_work = models.ForeignKey('works.TCCWork', verbose_name=_('tcc work'),
                                 on_delete=models.DO_NOTHING, related_name='tcc_work')

    class Meta:
        verbose_name = _('Work step')
        verbose_name_plural = _('Work steps')


class WorkStepVersion(models.Model):
    """
    Work step version model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('created at'))
    content = models.JSONField(verbose_name=_('content'))
    work_step = models.ForeignKey('works.WorkStep', verbose_name=_('work step'),
                                  on_delete=models.DO_NOTHING, related_name='step_version')

    class Meta:
        verbose_name = _('Work step version')
        verbose_name_plural = _('Work step versions')


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

    class Meta:
        verbose_name = _('Change request')
        verbose_name_plural = _('Change requests')
