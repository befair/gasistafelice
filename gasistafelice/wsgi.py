import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gasistafelice.settings')


from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

# After upgrading Django, replace the last 2 lines with the next two:
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()
