"""
Implementação dos models do app de meetings.

Contém os modelos de:
    - ApprovedMeeting (Pivô entre meeting e usuário);
    - Meeting (Reunião);
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.datetime import get_datetime_tz


class ApprovedMeeting(models.Model):
    """Modelo de ApprovedMeeting.

    Esta é a tabela pivô entre o relacionamento Many to Many
    entre reunião e usuário;
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    approved = models.BooleanField(verbose_name=_('approved'), null=True, default=None)
    meeting = models.ForeignKey(
        'meetings.Meeting', verbose_name=_('meeting'), on_delete=models.CASCADE, related_name='meeting_approved',
    )
    user = models.ForeignKey(
        'users.User', verbose_name=_('user'), on_delete=models.CASCADE, related_name='approved_meeting',
    )

    class Meta:
        verbose_name = _('Approved meeting')
        verbose_name_plural = _('Approved meetings')

    def __str__(self):
        return f'Aprovação: {self.user} - {self.approved}'


class Meeting(models.Model):
    """Modelo de reunião."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_('description'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    meeting_date = models.DateTimeField(verbose_name=_('meeting date'), blank=False, null=True)
    work_stage = models.ForeignKey(
        'works.FinalWorkStage', verbose_name=_('work stage'), on_delete=models.DO_NOTHING,
        related_name='stage_meeting',
    )
    participants = models.ManyToManyField(
        'users.User', related_name='meeting_participants',
        through='ApprovedMeeting',
    )
    developed_activities = models.TextField(
        verbose_name=_('Developed activities'), default='', blank=True,
    )
    instructions = models.TextField(verbose_name=_('Instructions'), default='', blank=True)

    class Meta:
        verbose_name = _('Metting')
        verbose_name_plural = _('Meetings')

    def get_is_approved(self):
        """Método que retorna o estado de aprovação de uma reunião."""
        approved_meeting = self.meeting_approved.all()

        is_approved = not approved_meeting.exclude(approved=True).exists()
        if is_approved:
            return True

        is_disapproved = approved_meeting.filter(approved=False).exists()
        if is_disapproved:
            return False

        return None

    def get_created_at(self):
        """Retorna o datetime de criação da reunião."""
        return get_datetime_tz(self.created_at).strftime("%d/%m/%Y %H:%M") if self.created_at is not None else None

    def get_meeting_date(self):
        """Retorna o datetime da reunião."""
        return get_datetime_tz(self.meeting_date).strftime("%d/%m/%Y %H:%M") if self.meeting_date is not None else None

    def review_meeting_required(self, user):
        """Verifica se um usuário precisa aprovar/desaprovar a reunião."""
        if user is None:
            raise Exception('User is required.')

        return self.meeting_approved.all().filter(approved=None, user=user).exists()

    def __str__(self):
        return f'Reunião: "{self.description}" às {self.get_meeting_date()} - {self.work_stage}'
