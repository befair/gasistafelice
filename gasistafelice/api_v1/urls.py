from django.conf.urls import patterns, include, url
from django.conf import settings

from . import views


urlpatterns = patterns('',

    url(r'^token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),

    url(r'^person/$', views.PersonCreateReadView.as_view(), name='api-v1-person-list'),
    url(r'^person/my/$', views.get_user_person, name='api-v1-person-user'),
    url(r'^person/(?P<pk>\d+)/$', views.PersonReadUpdateDeleteView.as_view(), name='api-v1-person'),
    # DEBUG USE WITH CARE! TODO TOMIKE (r'^gasmember/573/$', views.test573),
    (r'^gasmember/(?P<pk>\d+)/cash/$', views.GASMemberCashReadUpdateDeleteView.as_view()),
    (r'^gasmember/(?P<pk>\d+)/$', views.GASMemberReadUpdateDeleteView.as_view()),
    (r'^gas/(?P<pk>\d+)/$', views.GASReadUpdateDeleteView.as_view()),
    (r'^supplier/(?P<pk>\d+)/$', views.SupplierReadUpdateDeleteView.as_view()),
)
