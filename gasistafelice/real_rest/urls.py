
from django.conf.urls import patterns, include, url
from django.conf import settings

import views as rest_views
from rest_framework.authtoken import views

urlpatterns = patterns('',

    url(r'^v1/token-auth/', views.obtain_auth_token),

    url(r'^v1/person/$', rest_views.PersonCreateReadView.as_view(), name='api-v1-person-list'),
    url(r'^v1/person/my/$', rest_views.get_user_person, name='api-v1-person-user'),
    url(r'^v1/person/(?P<pk>\d+)/$', rest_views.PersonReadUpdateDeleteView.as_view(), name='api-v1-person'),
    # DEBUG USE WITH CARE! TODO TOMIKE (r'^v1/gasmember/573/$', rest_views.test573),
    (r'^v1/gasmember/(?P<pk>\d+)/cash/$', rest_views.GASMemberCashReadUpdateDeleteView.as_view()),
    (r'^v1/gasmember/(?P<pk>\d+)/$', rest_views.GASMemberReadUpdateDeleteView.as_view()),
    (r'^v1/gas/(?P<pk>\d+)/$', rest_views.GASReadUpdateDeleteView.as_view()),
    (r'^v1/supplier/(?P<pk>\d+)/$', rest_views.SupplierReadUpdateDeleteView.as_view()),
)
