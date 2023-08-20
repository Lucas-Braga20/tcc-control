"""
Users app models.
"""

import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from works.models import FinalWork


class User(AbstractUser):
    """
    User model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(verbose_name=_('phone'), max_length=14, blank=True, null=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_current_work(self):
        return FinalWork.objects.filter(mentees__in=[self.id]).order_by('-created_at').last()

    def __str__(self) -> str:
        return self.get_full_name()
