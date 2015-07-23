"""
WSGI config for gasistafelice project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from uwsgidecorators import timer


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gf.settings")
app = get_wsgi_application()

if settings.ENV in ('stage', 'prod'):

    @timer(600)
    def order_fix_state(sig):
        from django.core.management import call_command

        call_command('order_fix_state', interactive=False)

else:
    from django.utils import autoreload
    import uwsgi

    @timer(1)
    def change_code_graceful_reload(sig):
        if autoreload.code_changed():
            uwsgi.reload()
