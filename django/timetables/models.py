"""
Implementação dos models do app de timetables.

Contém os modelos de:
    - Timetables (Cronogramas);
    - Stage (Etapas);
    - StageExample (Documento de exemplos de etapa);
"""

import uuid
import os

from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _

from timetables.documents import get_template_folder


class Timetable(models.Model):
    """Modelo de Cronograma."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_('description'))
    teacher = models.ForeignKey(
        'users.User', related_name='teacher', verbose_name=_('teacher'),
        on_delete=models.DO_NOTHING,
    )
    participants = models.ManyToManyField(
        'users.User', related_name='participants',
        verbose_name=_('pariticipants'),
    )
    document_template = models.FileField(
        upload_to=get_template_folder, verbose_name=_('Document template'),
        blank=True, null=False,
    )
    archived = models.BooleanField(default=False, verbose_name=_('archived'))

    class Meta:
        verbose_name = _('Timetable')
        verbose_name_plural = _('Timetables')

    def __str__(self):
        return f"Cronograma: {self.description} - Professor: {self.teacher}"


class Stage(models.Model):
    """Modelo de Etapa do Cronograma."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_('description'))
    start_date = models.DateField(verbose_name=_('start date'))
    send_date_supervisor = models.DateField(verbose_name=_('send date supervisor'))
    send_date = models.DateField(verbose_name=_('send date'))
    presentation_date = models.DateField(verbose_name=_('presentation date'), blank=True, null=True)
    activity_configuration = models.ForeignKey(
        'activities.ActivityConfiguration', related_name='activity_configuration',
        verbose_name=_('activity configuration'), on_delete=models.DO_NOTHING,
    )
    timetable = models.ForeignKey(
        'timetables.TimeTable', related_name='stages', verbose_name=_('timetable'), on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = _('Stage')
        verbose_name_plural = _('Stages')

    def already_started(self):
        today = date.today()

        if today > self.start_date:
            return True

        if today > self.send_date_supervisor:
            return True

        if today > self.send_date:
            return True

        if self.presentation_date and today > self.presentation_date:
            return True

        return False

    def get_start_date(self):
        return self.start_date.strftime('%d/%m/%Y')

    def get_send_date_supervisor(self):
        return self.send_date_supervisor.strftime('%d/%m/%Y')

    def get_send_date(self):
        return self.send_date.strftime('%d/%m/%Y')

    def get_presentation_date(self):
        return self.presentation_date.strftime('%d/%m/%Y') if self.presentation_date is not None else None

    def __str__(self):
        return f"Etapa: {self.description} - Cronograma: {self.timetable}"


class StageExample(models.Model):
    """Modelo de documento de exemplo da etapa."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='documents/stage-example/', blank=True, null=True)
    stage = models.ForeignKey(
        'timetables.Stage', related_name='stage_examples', verbose_name=_('stage'), on_delete=models.CASCADE,
        blank=True, null=True,
    )

    class Meta:
        verbose_name = _('Stage example')
        verbose_name_plural = _('Stage examples')

    def get_file_name(self):
        return os.path.basename(self.file.name) if self.file is not None else None

    def get_file_size(self):
        return round(self.file.size / (1024 * 1024), 3) if self.file is not None else None

    def get_file_extension(self):
        return os.path.splitext(self.file.name)[1] if self.file is not None else None

    def __str__(self):
        return f"Documento: {self.file} - Etapa: {self.stage}"
