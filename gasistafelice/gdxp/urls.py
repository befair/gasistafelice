from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^suppliers/$', 'gdxp.views.suppliers'),
)
