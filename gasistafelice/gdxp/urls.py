from django.conf.urls.defaults import *
try:
    from django.conf.urls import url
except ImportError as e:
    # Using Django < 1.4
    from django.conf.urls.defaults import url

urlpatterns = patterns('',
    (r'^suppliers/$', 'gdxp.views.suppliers'),
)
