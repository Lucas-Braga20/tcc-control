import os

from django.utils.text import slugify


def slugify_filename(filename):
    """Retorna o nome de um arquivo em forma de slug."""
    basename, ext = os.path.splitext(filename)
    slug = slugify(basename)
    return f'{slug}{ext}'