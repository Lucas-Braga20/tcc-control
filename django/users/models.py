"""Modelos do app de usuários."""

import uuid

import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from works.models import FinalWork
from timetables.models import Timetable


class User(AbstractUser):
    """Modelo de usuário."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(
        verbose_name=_('phone'), max_length=14, blank=True, null=True,
    )
    rgm = models.CharField(
        verbose_name=_('RGM'), max_length=20, default='', blank=True,
    )
    university_course = models.ForeignKey(
        'courses.Course', verbose_name=_('University course'),
        on_delete=models.DO_NOTHING, related_name='course',
        blank=True, null=True,
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_current_work(self):
        return FinalWork.objects.filter(mentees__in=[self.id], archived=False).order_by('-created_at').last()

    def get_profile_url(self):
        return reverse('users:profile', kwargs={'pk': self.id})

    def get_already_in_work(self):
        return self.work_mentee.filter(archived=False, completed=False).exists()

    def get_current_timetable(self):
        timetables = self.participants.all()

        if timetables.exists() is False:
            return None

        return timetables.last()

    def __str__(self) -> str:
        return self.get_full_name()
