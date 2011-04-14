from django.conf.urls.defaults import *

# Base generic admin site for superusers
from django.contrib import admin
admin.autodiscover()

from gasistafelice.gas_admin.models import gas_admin

urlpatterns = patterns('',
    # Example:
    # (r'^gasistafelice/', include('gasistafelice.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^gas-admin/', include(gas_admin.urls)),

    (r'^admin/', include(admin.site.urls)),
)
