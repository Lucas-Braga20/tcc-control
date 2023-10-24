"""Utilitários do app de works."""

import os

import datetime

from django.conf import settings
from django.utils import timezone

from core.files import slugify_filename


def validate_stage_content_json(content):
    """Valida o conteúdo da etapa.

    O campo json deve conter o atributo "fields" como array de objetos
    contém os atributos: chave e valor.
    """

    fields = content.get('fields')

    if fields is None:
        raise Exception('O campo "fields" não pode ser nulo.')

    for field in fields:
        key = field.get('key')
        value = field.get('value')

        if key is None or value is None:
            raise Exception('Um campo não foi inserido corretamente.')


def get_version_content_image_folder(instance, filename):
    """Recupera o diretório de upload da imagem do desenvolvimento."""
    new_filename = slugify_filename(filename)

    return f'works/{instance.version.work_stage.final_work.id}/versions/{instance.version.id}/${new_filename}'


def get_document_creation_time(document_path, concat=True):
    """Recupera o datetime de criação do documento final."""
    if concat:
        file_path = os.path.join(settings.BASE_DIR, 'tcc_control', document_path)
    else:
        file_path = document_path

    stat = os.stat(file_path)

    try:
        creation_time = stat.st_birthtime
    except AttributeError:
        creation_time = stat.st_mtime

    tz = timezone.get_default_timezone()

    dt_object = timezone.make_aware(datetime.datetime.fromtimestamp(creation_time), tz)

    return dt_object
