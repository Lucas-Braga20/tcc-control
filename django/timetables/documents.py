"""Utilitários de documentos.

Contém todas as funções utilitárias para tratar documentos no módulo de
TimeTable.
"""


def get_template_folder(instance, filename):
    """Recupera o caminho do template."""
    return f'timetables/{instance.id}/templates/${filename}'
