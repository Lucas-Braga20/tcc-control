from celery import shared_task

from notifications.utils import send_tcc_mail


@shared_task
def send_mail(description, subject, receivers):
    # Envia emails.
    send_tcc_mail(
        context={
            'message': description,
            'subject': subject,
        },
        receivers=receivers
    )
