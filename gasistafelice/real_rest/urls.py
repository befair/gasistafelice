
from django.conf.urls import patterns, include, url
from django.conf import settings

import views as rest_views

urlpatterns = patterns('',

    url(r'^v1/person/$', rest_views.PersonCreateReadView.as_view(), name='api-v1-person-list'),
    url(r'^v1/person/my/$', rest_views.get_user_person, name='api-v1-person-user'),
    url(r'^v1/person/(?P<pk>\d+)/$', rest_views.PersonReadUpdateDeleteView.as_view(), name='api-v1-person'),
    (r'^v1/gasmember/(?P<pk>\d+)/$', rest_views.GASMemberReadUpdateDeleteView.as_view()),
    (r'^v1/gas/(?P<pk>\d+)/$', rest_views.GASReadUpdateDeleteView.as_view()),
    (r'^v1/supplier/(?P<pk>\d+)/$', rest_views.SupplierReadUpdateDeleteView.as_view()),
)
