import pytz

from tcc_control.settings import TIME_ZONE


def get_datetime_tz(date_without_tz):
    timezone = pytz.timezone(TIME_ZONE)

    return date_without_tz.astimezone(timezone)
