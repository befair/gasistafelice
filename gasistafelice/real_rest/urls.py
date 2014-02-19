
from django.conf.urls.defaults import *
from django.conf import settings

import views as rest_views

urlpatterns = patterns('',

    (r'^v1/person/$', rest_views.PersonCreateReadView.as_view()),
    (r'^v1/person/(?P<pk>\d+)/$', rest_views.PersonReadUpdateDeleteView.as_view()),
    (r'^v1/gas/(?P<pk>\d+)/$', rest_views.GASReadUpdateDeleteView.as_view()),
)
