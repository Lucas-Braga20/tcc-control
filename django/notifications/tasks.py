"""
Implementação dos Tasks assíncronas do app de notifications.

Contém as tasks de:
    - send_mail (Enviar email);
"""

from celery import shared_task

from notifications.utils import send_tcc_mail


@shared_task
def send_mail(description, subject, receivers):
    """Task de envio de emails.

    Essa task foi implementada para que a request funcione
    de maneira assíncrona.

    Por exemplo: ao marcar como completado uma etapa. Um email
    é enviado através de uma task do scheduler para que o response
    da requisição não dependa do retorno da função send_mail e tenha
    que aguardar.
    """

    # Envia emails.
    send_tcc_mail(
        context={
            'message': description,
            'subject': subject,
        },
        receivers=receivers
    )
