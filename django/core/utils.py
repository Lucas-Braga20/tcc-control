import pytz

from datetime import date

from timetables.models import Timetable
from works.models import FinalWorkStage

from tcc_control.settings import TIME_ZONE


def generate_work_stages(final_work):
    if not final_work:
        raise Exception('Final work is required.')

    today = date.today()

    timetable = Timetable.objects.filter(stages__start_date__lte=today, stages__send_date__gte=today, archived=False)

    if not timetable.exists():
        raise Exception('There is no active timetable')

    timetable = timetable.first()

    stages = timetable.stages.all()

    stages_already_generated = final_work.work_stage.all()

    for stage in stages:
        if not stages_already_generated.filter(stage=stage).exists():
            final_work_stage = FinalWorkStage(presented=False, stage=stage, final_work=final_work)
            final_work_stage.save()


def get_datetime_tz(date_without_tz):
    timezone = pytz.timezone(TIME_ZONE)

    return date_without_tz.astimezone(timezone)
