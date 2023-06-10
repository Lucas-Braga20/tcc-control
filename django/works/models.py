"""
Works models include TCC and development step.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core import defaults


class TCCWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_('description'))
    approved = models.BooleanField(verbose_name=_('approved'), default=False)
    advisor = models.ForeignKey('users.User', related_name='advisor', verbose_name=_('advisor'),
                                on_delete=models.DO_NOTHING)
    advised = models.ManyToManyField('users.User', related_name='advised',
                                     verbose_name=_('advised'))


class WorkStep(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    presented = models.BooleanField(verbose_name=_('presented'), default=False)
    status = models.SmallIntegerField(verbose_name=_('status'),
                                      choices=defaults.WORK_STEP_STATUS,
                                      default=defaults.WORK_STEP_ASSIGNED)
    step = models.ForeignKey('timetables.Step', verbose_name=_('step'),
                             on_delete=models.DO_NOTHING, related_name='step')
