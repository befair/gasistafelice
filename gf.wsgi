import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'gasistafelice.settings'

sys.path = ['', '/var/www/gf_ria/gasistafelice/', '/var/www/gf_ria/', '/var/www/gf_ria/gfenv/src/django-pro-history', '/var/www/gf_ria/gfenv/src/django-simple-accounting', '/var/www/gf_ria/gfenv/src/django-flexi-auth', '/var/www/gf_ria/gfenv/src/django-notification', '/var/www/gf_ria/gfenv/src/xhtml2pdf', '/var/www/gf_ria/gfenv/lib/python2.7', '/var/www/gf_ria/gfenv/lib/python2.7/plat-x86_64-linux-gnu', '/var/www/gf_ria/gfenv/lib/python2.7/lib-tk', '/var/www/gf_ria/gfenv/lib/python2.7/lib-old', '/var/www/gf_ria/gfenv/lib/python2.7/lib-dynload', '/usr/lib/python2.7', '/usr/lib/python2.7/plat-x86_64-linux-gnu', '/usr/lib/python2.7/lib-tk', '/var/www/gf_ria/gfenv/local/lib/python2.7/site-packages', '/var/www/gf_ria/gfenv/local/lib/python2.7/site-packages/PIL', '/var/www/gf_ria/gfenv/lib/python2.7/site-packages', '/var/www/gf_ria/gfenv/lib/python2.7/site-packages/PIL']

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
