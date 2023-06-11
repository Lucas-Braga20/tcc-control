"""
Meeting app models.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class ApprovedMeeting(models.Model):
    """
    Approved meetings model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    approved = models.BooleanField(verbose_name=_('approved'), default=False)
    meeting = models.ForeignKey('meetings.Meeting', verbose_name=_('meeting'),
                                on_delete=models.CASCADE, related_name='meeting_approved')
    user = models.ForeignKey('users.User', verbose_name=_('user'),
                             on_delete=models.CASCADE, related_name='approved_meeting')

    class Meta:
        verbose_name = _('Approved meeting')
        verbose_name_plural = _('Approved meetings')


class Meeting(models.Model):
    """
    Meeting model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_('description'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('created at'))
    work_step = models.ForeignKey('works.WorkStep', verbose_name=_('work step'),
                                  on_delete=models.DO_NOTHING, related_name='step_meeting')
    participants = models.ManyToManyField('users.User', related_name='meeting_participants',
                                          through='ApprovedMeeting')

    class Meta:
        verbose_name = _('Metting')
        verbose_name_plural = _('Meetings')
