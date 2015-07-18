"""
WSGI config for gasistafelice project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gf.settings")
app = get_wsgi_application()

if settings.ENV == 'dev':
    from django.utils import autoreload
    import uwsgi
    from uwsgidecorators import timer

    @timer(1)
    def change_code_graceful_reload(sig):
        if autoreload.code_changed():
            uwsgi.reload()
