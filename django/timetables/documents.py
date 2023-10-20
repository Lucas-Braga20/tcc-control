"""Utilitários de documentos.

Contém todas as funções utilitárias para tratar documentos no módulo de
TimeTable.
"""

from django.utils.text import slugify


def get_template_folder(instance, filename):
    """Recupera o caminho do template."""
    new_filename = slugify(filename)

    return f'timetables/{instance.id}/templates/${new_filename}'
