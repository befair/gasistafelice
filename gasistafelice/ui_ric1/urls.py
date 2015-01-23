# Copyright beFair http://www.befair.it
# Part of project Gasista Felice
# License: AGPLv3

from django.conf.urls.defaults import *

urlpatterns = patterns('ui_ric1.views',

    # Main page
    url(r'^$', 'index', name="page_ui_ric1"),
    
)


