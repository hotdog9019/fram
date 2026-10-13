"""WSGI config for HackFlow."""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hackflow_site.settings")

application = get_wsgi_application()
