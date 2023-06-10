"""
Activities Models.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class ActivityConfiguration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fields = models.JSONField(verbose_name=_("Fields"))
    template_abnt = models.FileField(upload_to='documents/', blank=True, null=True)
