import datetime
import os

from django.utils.text import slugify

from core import defaults

from works.models import FinalWorkStage


def generate_work_stages(final_work, timetable):
    if not final_work:
        raise Exception('Final work is required.')
    
    if not timetable:
        raise Exception('Timetable is required.')

    stages = timetable.stages.all()

    stages_already_generated = final_work.work_stage.all()

    for stage in stages:
        if not stages_already_generated.filter(stage=stage).exists():
            final_work_stage = FinalWorkStage(presented=False, stage=stage, final_work=final_work)
            final_work_stage.save()


def process_stage_status(final_work):
    # today = datetime.date.today()
    today = datetime.date(2023, 1, 1)

    stages = final_work.work_stage.all()

    late = stages.filter(status__in=defaults.NOT_COMPLETED_STATUS, stage__send_date__lt=today)

    for stage in late:
        stage.status = defaults.WORK_STAGE_PENDING
        stage.save()


def slugify_filename(filename):
    """Retorna o nome de um arquivo em forma de slug."""
    basename, ext = os.path.splitext(filename)
    slug = slugify(basename)
    return f'{slug}{ext}'
