from django.conf.urls.defaults import *
from django.conf import settings

# Base generic admin site for superusers
from django.contrib import admin
admin.autodiscover()

from gasistafelice.gas_admin.models import gas_admin

urlpatterns = patterns('',

	(r'^$'       , 'base.views.index'  ),
	(r'^%s$'     % settings.URL_PREFIX , 'base.views.index'  ),
	(r'^%srest/' % settings.URL_PREFIX, include('rest.urls')),

	(r'^%saccounts/login/$' % settings.URL_PREFIX, 'django.contrib.auth.views.login'),

    (r'^gas/$', 'gas.views.index'),

    (r'^gas-admin/', include(gas_admin.urls)),

    (r'^admin/', include(admin.site.urls)),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

