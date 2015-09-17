from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin


js_info_dict = {
    'domain': 'djangojs',
    'packages': ('gasistafelice.localejs', ),
}

urlpatterns = patterns('',

    (r'^gasistafelice/$', 'gf.base.views.index'),
    (r'^gasistafelice/simulate_user/(?P<user_pk>\d+)/$', 'gf.base.views.simulate_user'),

    #New user interface
    (r'^gasistafelice/gas/', include('gf.gas.urls')),
    #(r'^gasistafelice/supplier/', include('gf.supplier.urls')),
    #(r'^gasistafelice/order/', include('gf.gas.order_urls')),

    #End new user interface
    (r'^gasistafelice/rest/', include('rest.urls')),

    (r'^gasistafelice/accounts/login/$', 'des.views.login'),
    (r'^gasistafelice/accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^gasistafelice/accounts/registration/$', 'des.views.registration'),
    url(r'^gasistafelice/activate/(?P<activation_key>\w+)/$',
        'des.views.activate', name='registration_activate'),
    (r'^gasistafelice/accounts/reserved_registration/$', 'des.views.staff_registration'),

    (r'^gasistafelice/admin/', include(admin.site.urls)),

    (r'^gasistafelice/jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    #url(r"^gasistafelice/notices/", include("notification.urls")),
    (r'^gasistafelice/lookups/', include('ajax_select.urls')),

    (r'^gasistafelice/gdxp/', include('gdxp.urls')),
    (r'^api/v1/', include('api_v1.urls')),
    (r'^api/remote/', include('api_remote.urls')),
)

urlpatterns += patterns('',
    url(r'^gasistafelice/captcha/', include('captcha.urls')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^gasistafelice/rosetta/', include('rosetta.urls')),
    )

if settings.ENV == 'dev':
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
