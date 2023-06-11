"""
Activities app models.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class ActivityConfiguration(models.Model):
    """
    Activitiy confifugration model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fields = models.JSONField(verbose_name=_("Fields"))
    template_abnt = models.FileField(upload_to='documents/', blank=True, null=True)

    class Meta:
        verbose_name = _('Activity Configuration')
        verbose_name_plural = _('Activity Configurations')

    def __str__(self):
        return str(id)
