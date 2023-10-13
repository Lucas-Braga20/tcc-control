import datetime

from django.db.models import Q

from celery import shared_task

from notifications.utils import send_notification
from notifications.tasks import send_mail
from timetables.models import Timetable
from works.models import FinalWorkStage

from core.utils import generate_work_stages, process_stage_status
from core.defaults import completed_status


@shared_task
def process_final_works():
    today = datetime.date.today()
    # today hard coded
    # today = datetime.date(2023, 1, 1)

    timetables = Timetable.objects.filter(
        Q(stages__start_date__lte=today) | Q(stages__send_date__gte=today), archived=False,
    )

    for timetable in timetables:
        final_works = timetable.timetable_works.all()

        for final_work in final_works:
            # Generate work stages for all final works.
            generate_work_stages(final_work=final_work, timetable=timetable)

            # Process Stage status
            process_stage_status(final_work=final_work)


@shared_task()
def send_notifications():
    today = datetime.date.today()

    tomorrow = datetime.timedelta(days=1) + today

    send_to_supervisor = FinalWorkStage.objects.filter(
        Q(stage__send_date_supervisor=tomorrow)
    ).exclude(status__in=completed_status)

    for work in send_to_supervisor:
        description = f'Amanhã é a data de entrega ao supervisor da etapa: "{work.stage.description}"'

        receivers = []
        receivers.append(work.final_work.supervisor)
        receivers += list(work.final_work.mentees.all())

        send_notification(
            description=description,
            author=None,
            receivers=receivers,
        )

        send_mail.delay(
            description,
            'Data de entrega ao supervisor',
            [{
                'name': receiver.get_full_name(),
                'email': receiver.email,
            } for receiver in receivers],
        )

    send_date = FinalWorkStage.objects.filter(
        Q(stage__send_date=tomorrow)
    ).exclude(status__in=completed_status)

    for work in send_date:
        description = f'Amanhã é a data de entrega da etapa: "{work.stage.description}"'

        receivers = []
        receivers.append(work.final_work.supervisor)
        receivers += list(work.final_work.mentees.all())

        send_notification(
            description=description,
            author=None,
            receivers=receivers,
        )

        send_mail.delay(
            description,
            'Data de entrega',
            [{
                'name': receiver.get_full_name(),
                'email': receiver.email,
            } for receiver in receivers],
        )

    presentation_date = FinalWorkStage.objects.filter(
        Q(stage__presentation_date=tomorrow)
    ).exclude(status__in=completed_status)

    for work in presentation_date:
        description = f'Amanhã é a data de apresentação da etapa: "{work.stage.description}"'

        receivers = []
        receivers.append(work.final_work.supervisor)
        receivers += list(work.final_work.mentees.all())

        send_notification(
            description=description,
            author=None,
            receivers=receivers,
        )

        send_mail.delay(
            description,
            'Data de apresentação',
            [{
                'name': receiver.get_full_name(),
                'email': receiver.email,
            } for receiver in receivers],
        )
