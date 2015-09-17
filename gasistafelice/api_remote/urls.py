from django.conf.urls import patterns, include, url

from api_remote.views import proxy

urlpatterns = patterns('',
    url(r'^(?P<backend_name>\w+)/(?P<remote_path>.*)', proxy, name='api-remote-proxy'),
)
