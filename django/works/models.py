"""
Works app models.
"""

import uuid
import os

from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings

from core import defaults
from core.datetime import get_datetime_tz

from works.utils import get_version_content_image_folder
from works.document.json_to_docx import JsonToDocx


class FinalWork(models.Model):
    """
    Final work model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_('description'))
    approved = models.BooleanField(
        verbose_name=_('approved'), null=True, blank=True,
    )
    supervisor = models.ForeignKey(
        'users.User', related_name='work_supervisor',
        verbose_name=_('supervisor'), on_delete=models.DO_NOTHING,
    )
    mentees = models.ManyToManyField(
        'users.User', related_name='work_mentee', verbose_name=_('mentee'),
    )
    timetable = models.ForeignKey(
        'timetables.Timetable', related_name='timetable_works',
        verbose_name=_('timetable'), on_delete=models.DO_NOTHING,
        null=True,
    )
    archived = models.BooleanField(default=False, verbose_name=_('archived'))
    completed = models.BooleanField(default=False, verbose_name=_('completed'))
    grading_score = models.SmallIntegerField(
        default=0, verbose_name=_('grading score'),
    )
    able_to_present = models.BooleanField(
        default=None, null=True, verbose_name=_('able to present'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'),
        blank=True, null=True,
    )

    class Meta:
        verbose_name = _('Final work')
        verbose_name_plural = _('Final works')

    def get_mentees(self):
        return ', '.join([mentee.get_full_name() for mentee in self.mentees.all()])

    def get_current_stage(self):
        today = date.today()

        stage = self.work_stage.filter(stage__start_date__lte=today, stage__send_date__gte=today)

        if not stage.exists():
            return self.work_stage.filter().order_by('-stage__send_date').first()

        return stage.first()

    def get_final_work_url(self):
        return reverse('works:stages', kwargs={'pk': self.id})

    def get_all_content_data(self, filter_insertion=True):
        work_stages = self.work_stage.all()

        all_fields = []

        for work_stage in work_stages:
            # Pula etapas em que a atividade não possua inclusão.
            document_insertion = work_stage.stage.activity_configuration.document_insertion
            if filter_insertion is True and document_insertion is False:
                continue

            last_version = work_stage.get_last_version()

            if last_version:
                all_fields = all_fields + last_version.content.get('fields', [])

        return {
            'fields': all_fields + [
                {'key': 'coordenador', 'value': 'Felipe'},
                {'key': 'titulo', 'value': 'TESTEEEEEEE'},
                {'key': 'aluno', 'value': 'Lucas'},
                {'key': 'orientador', 'value': 'Felipe'},
            ],
        }

    def get_template_document(self):
        if self.timetable is None:
            return None

        return os.path.join(settings.MEDIA_ROOT, str(self.timetable.document_template))

    def generate_final_document(self):
        template = self.get_template_document()
        content = self.get_all_content_data()

        output_path_docx = os.path.join(
            settings.MEDIA_ROOT,
            f'works/{self.id}/final_documents/{uuid.uuid4()}.docx',
        )

        if template:
            try:
                json_to_docx = JsonToDocx(template, content, output_path_docx)

                return json_to_docx.convert()
            except:
                return None

        return None

    def get_final_documents(self):
        final_documents_dir = f'works/{self.id}/final_documents/'
        media_dir = os.path.join(f'media/works/{self.id}/final_documents/')
        final_documents_dir = os.path.join(settings.MEDIA_ROOT, final_documents_dir)

        try:
            documents = [
                os.path.join(media_dir, document) for document in os.listdir(final_documents_dir)
                if os.path.isfile(os.path.join(final_documents_dir, document))
            ]
        except:
            documents = []

        return documents

    def __str__(self):
        return f'TCC: "{self.description}"'


class FinalWorkStage(models.Model):
    """
    Final work stage model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    presented = models.BooleanField(verbose_name=_('presented'), default=False)
    status = models.IntegerField(verbose_name=_('status'),
                                 choices=defaults.WORK_STAGE_STATUS,
                                 default=defaults.WORK_STAGE_ASSIGNED)
    stage = models.ForeignKey('timetables.Stage', verbose_name=_('time table stage'),
                              on_delete=models.DO_NOTHING, related_name='work_timetable_stage')
    final_work = models.ForeignKey('works.FinalWork', verbose_name=_('final work'),
                                   on_delete=models.DO_NOTHING, related_name='work_stage')

    class Meta:
        verbose_name = _('Final work stage')
        verbose_name_plural = _('Final work stages')

    def get_date_state(self):
        today = date.today()

        if self.stage.send_date < today:
            return 'Etapa passada'

        if self.stage.start_date > today:
            return 'Etapa futura'

        return 'Etapa atual'

    def get_last_version(self):
        return self.work_stage_version.all().order_by('-created_at').first()

    def __str__(self):
        return f'Etapa do {self.final_work.description}: "{self.stage.description}"'


class FinalWorkVersion(models.Model):
    """Final work version model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('created at'))
    content = models.JSONField(verbose_name=_('content'), blank=True, null=True)
    confirmed = models.BooleanField(verbose_name=_('confirmed'), default=False)
    work_stage = models.ForeignKey('works.FinalWorkStage', verbose_name=_('work stage'),
                                   on_delete=models.DO_NOTHING, related_name='work_stage_version')

    class Meta:
        verbose_name = _('Work stage version')
        verbose_name_plural = _('Work stage versions')

    def get_is_blocked(self):
        stage = self.work_stage
        versions = stage.work_stage_version.all().order_by('created_at')

        if self != versions.last():
            return True

        if self.work_stage.status in defaults.completed_status:
            return True

        return False

    def __str__(self):
        return f'Versão: "{self.work_stage}"'


class VersionContentImage(models.Model):
    """
    Version content image model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=get_version_content_image_folder, verbose_name=_('image'), max_length=255)
    version = models.ForeignKey('works.FinalWorkVersion', verbose_name=_('work version'),
                                on_delete=models.CASCADE, related_name='version_images')

    def __str__(self):
        return f'Imagem da versão: "{self.version}"'


class ChangeRequest(models.Model):
    """
    Change request model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    approved = models.BooleanField(verbose_name=_('approved'), blank=True, null=True, default=None)
    description = models.TextField(verbose_name=_('description'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('created at'))
    requester = models.ForeignKey('users.User', verbose_name=_('requester'),
                                  on_delete=models.DO_NOTHING, related_name='requester')
    work_stage = models.ForeignKey('works.FinalWorkStage', verbose_name=_('work stage'),
                                   on_delete=models.DO_NOTHING, related_name='work_stage_change_request')

    class Meta:
        verbose_name = _('Change request')
        verbose_name_plural = _('Change requests')

    def approve_request(self):
        """
        Method to approve a change request.
        """
        self.approved = True
        new_version = FinalWorkVersion(content=None, work_stage=self.work_stage)
        self.save()
        new_version.save()

    def get_created_at(self):
        return get_datetime_tz(self.created_at).strftime("%d/%m/%Y %H:%M") if self.created_at is not None else None

    def __str__(self):
        return f'Solicitação de alteração: "{self.work_stage}"'
