"""
Users app models.
"""

import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    User model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(verbose_name=_('phone'), max_length=14, blank=True, null=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
