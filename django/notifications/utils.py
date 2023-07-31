"""
Funções utilitárias para o app de notificações.
"""

from notifications.serializers import NotificationSerializer

from users.models import User


def send_notification(description, receivers, author=None):
    """Envia notificação e email.

    Args:
        description (str): [Conteúdo da notificação]
        receivers (User): [Usuários destinatários da notificação]
        author (User | None): [Usuário responsável pela notificação]

    Returns:
        [NotificationSerializer]: [Serializer do model de Notificação]
    """

    # Quando a notificação é disparada pelo sistema a autoria é da administração.
    if author is None:
        author = User.objects.get(username='admin')

    # Cria notificações internas.
    notification_serializer = NotificationSerializer(data={
        'description': description,
        'author': author.id,
        'receiver': [receiver.id for receiver in receivers],
    })
    notification_serializer.is_valid(raise_exception=True)
    notification_serializer.save()

    # TODO: Desenvolver o envio de e-mails.
    emails = []
    emails.append(author.email)
    emails += [receiver.email for receiver in receivers]

    return notification_serializer
