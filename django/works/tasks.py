from celery import shared_task

from notifications.serializers import NotificationSerializer
from users.models import User


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
