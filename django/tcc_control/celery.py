"""Configuração do celery do projeto TCC Control."""

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tcc_control.settings')

app = Celery('tcc_control')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()
