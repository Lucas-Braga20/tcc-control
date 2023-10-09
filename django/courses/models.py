"""Modelos do app de cursos."""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    """Modelo de curso."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(
        verbose_name=_('description'), max_length=255,
    )
    archived = models.BooleanField(default=False, verbose_name=_('archived'))

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def __str__(self):
        return self.description
