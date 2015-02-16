from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin

from gas_admin.models import gas_admin

js_info_dict = {
    'domain'  : 'djangojs',
    'packages' : ('gasistafelice.localejs', ),
}

urlpatterns = patterns('',

	(r'^$'       , 'app_base.views.index'  ),
	(r'^%s$' % settings.URL_PREFIX , 'app_base.views.index'  ),
	(r'^%ssimulate_user/(?P<user_pk>\d+)/$' % settings.URL_PREFIX , 'app_base.views.simulate_user'  ),

    #New user interface
	(r'^%sgas/' % settings.URL_PREFIX, include('app_gas.urls')),
	#(r'^%ssupplier/' % settings.URL_PREFIX, include('app_supplier.urls')),
	#(r'^%sorder/' % settings.URL_PREFIX, include('app_gas.order_urls')),
    
    #End new user interface
	(r'^%srest/' % settings.URL_PREFIX, include('rest.urls')),

	(r'^%saccounts/login/$' % settings.URL_PREFIX, 'des.views.login'),
	(r'^%saccounts/logout/$' % settings.URL_PREFIX, 'django.contrib.auth.views.logout_then_login'),
	(r'^%saccounts/registration/$' % settings.URL_PREFIX, 'des.views.registration'),
    url(r'^%sactivate/(?P<activation_key>\w+)/$' % settings.URL_PREFIX,
        'des.views.activate', name='registration_activate'),
	(r'^%saccounts/reserved_registration/$' % settings.URL_PREFIX, 'des.views.staff_registration'),

    (r'^gas-admin/', include(gas_admin.urls)),
    (r'^%sadmin/' % settings.URL_PREFIX, include(admin.site.urls)),

	(r'^%sjsi18n/$'% settings.URL_PREFIX, 'django.views.i18n.javascript_catalog', js_info_dict),

    url(r"^%snotices/" % settings.URL_PREFIX, include("notification.urls")),
    (r'^%slookups/' % settings.URL_PREFIX, include('ajax_select.urls')),
)

urlpatterns += patterns('',
    url(r'^%scaptcha/' % settings.URL_PREFIX, include('captcha.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^%srosetta/' % settings.URL_PREFIX, include('rosetta.urls')),
    )
