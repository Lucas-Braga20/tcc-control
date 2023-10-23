"""Utilitários de datetime do app core."""

import pytz

from tcc_control.settings import TIME_ZONE


def get_datetime_tz(date_without_tz):
    """Recupera um datetime com o valor de timezone do servidor."""
    timezone = pytz.timezone(TIME_ZONE)

    return date_without_tz.astimezone(timezone)
