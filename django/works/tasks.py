import datetime

from django.db.models import Q

from celery import shared_task

from notifications.serializers import NotificationSerializer
from users.models import User
from timetables.models import Timetable
from works.models import FinalWork

from core import defaults
from core.utils import generate_work_stages, process_stage_status


@shared_task
def generate_works():
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
    author = User.objects.get(username='lucas.braga')
    receiver = User.objects.filter(username='admin')

    serializer = NotificationSerializer(data={
        'author': author.id,
        'receiver': [user.id for user in receiver],
        'description': 'teste'
    })

    serializer.is_valid(raise_exception=True)

    instance = serializer.save()

    print(instance)
