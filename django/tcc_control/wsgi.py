"""
WSGI config for tcc_control project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tcc_control.settings')

application = get_wsgi_application()
