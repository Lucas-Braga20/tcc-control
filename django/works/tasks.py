import datetime

from django.db.models import Q

from celery import shared_task

from notifications.serializers import NotificationSerializer
from notifications.utils import send_notification
from users.models import User
from timetables.models import Timetable
from works.models import FinalWork, FinalWorkStage

from core.utils import generate_work_stages, process_stage_status
from core.defaults import completed_status


@shared_task
def process_final_works():
    # today = datetime.date.today()
    today = datetime.date(2023, 3, 4)

    timetables = Timetable.objects.filter(stages__start_date__lte=today, stages__send_date__gte=today, archived=False)

    for timetable in timetables:
        mentees = timetable.participants.filter(groups__name='Orientando')

        final_works = FinalWork.objects.filter(archived=False, mentees__in=list(mentees.values_list('id'))).distinct()

        for final_work in final_works:
            # Generate work stages for all final works.
            generate_work_stages(final_work=final_work, timetable=timetable)

            # Process Stage status
            process_stage_status(final_work=final_work)


@shared_task()
def send_notifications():
    today = datetime.date.today()
    # today = datetime.date(2023, 6, 26)

    tomorrow = datetime.timedelta(days=1) + today

    send_to_supervisor = FinalWorkStage.objects.filter(
        Q(stage__send_date_supervisor=tomorrow)
    ).exclude(status__in=completed_status)

    for work in send_to_supervisor:
        receivers = []
        receivers.append(work.final_work.supervisor)
        receivers += list(work.final_work.mentees.all())
        send_notification(
            description=f'Amanhã é a data de entrega ao supervisor da etapa: "{work.stage.description}"',
            author=None,
            receivers=receivers
        )

    send_date = FinalWorkStage.objects.filter(
        Q(stage__send_date=tomorrow)
    ).exclude(status__in=completed_status)

    for work in send_date:
        receivers = []
        receivers.append(work.final_work.supervisor)
        receivers += list(work.final_work.mentees.all())
        send_notification(
            description=f'Amanhã é a data de entrega da etapa: "{work.stage.description}"',
            author=None,
            receivers=receivers
        )

    presentation_date = FinalWorkStage.objects.filter(
        Q(stage__presentation_date=tomorrow)
    ).exclude(status__in=completed_status)

    for work in presentation_date:
        receivers = []
        receivers.append(work.final_work.supervisor)
        receivers += list(work.final_work.mentees.all())
        send_notification(
            description=f'Amanhã é a data de apresentação da etapa: "{work.stage.description}"',
            author=None,
            receivers=receivers
        )
