"""Utilitários de datetime do app core."""

import pytz

from django.conf import settings


def get_datetime_tz(date_without_tz):
    """Recupera um datetime com o valor de timezone do servidor."""
    timezone = pytz.timezone(settings.TIME_ZONE)

    return date_without_tz.astimezone(timezone)
