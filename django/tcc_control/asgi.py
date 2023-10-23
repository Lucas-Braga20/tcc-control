"""ASGI configuração para o projeto TCC Control."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tcc_control.settings')

application = get_asgi_application()
