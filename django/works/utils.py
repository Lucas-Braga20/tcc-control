"""
Utils to works app.
"""

import os

import datetime

from django.conf import settings
from django.utils import timezone

from core.utils import slugify_filename


def validate_stage_content_json(content):
    """
    Method to validate field content.

    The json field must contain the attribute "fields" as array of objects
    contains the attributes: key and value.
    """

    fields = content.get('fields')

    if fields is None:
        raise Exception('The "fields" field cannot be null.')

    for field in fields:
        key = field.get('key')
        value = field.get('value')

        if key is None or value is None:
            raise Exception('A field was not entered correctly.')


def get_version_content_image_folder(instance, filename):
    """
    Get upload folder.
    """
    new_filename = slugify_filename(filename)

    return f'works/{instance.version.work_stage.final_work.id}/versions/{instance.version.id}/${new_filename}'


def get_document_creation_time(document_path, concat=True):
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
