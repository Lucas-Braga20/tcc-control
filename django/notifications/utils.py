"""
Funções utilitárias para o app de notificações.
"""

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from users.models import User
from notifications.serializers import NotificationSerializer


def send_tcc_mail(
        context, receivers, template_name='emails/index.html', from_email=settings.EMAIL_HOST_USER
    ):
    """Envia um email usando um template HTML no Django.

    Args:
        context (dict): Um dicionário com as variáveis de contexto para o template.
        receivers (list): Uma lista de destinatários (Nome e email).
        template_name (str): O nome do arquivo de template HTML.
        from_email (str): O endereço de email remetente.

    Retorna:
        bool: True se o email for enviado com sucesso, False em caso de erro.
    """
    try:
        for receiver in receivers:
            internal_context = context
            internal_context['receiver'] = receiver.get('name')

            html_message = render_to_string(template_name, internal_context)

            msg = EmailMultiAlternatives(context.get('subject'), html_message, from_email, [receiver.get('email')])
            msg.content_subtype = "html"
            msg.send()

        return True
    except Exception as e:
        return False


def send_notification(description, receivers, author=None):
    """Envia notificação.

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

    return notification_serializer
