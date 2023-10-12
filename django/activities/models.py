"""
Implementação dos models do app de atividades.

Contém os modelos de:
    - ActivityConfiguration (Configuração de atividade);
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class ActivityConfiguration(models.Model):
    """Modelo de Configuração de atividade."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(verbose_name=_('name'), max_length=255)
    fields = models.JSONField(verbose_name=_('fields'))
    document_insertion = models.BooleanField(verbose_name=_('Document insertion'), default=True)
    archived = models.BooleanField(default=False, verbose_name=_('archived'))

    class Meta:
        verbose_name = _('Activity Configuration')
        verbose_name_plural = _('Activity Configurations')

    def __str__(self):
        return str(id)
