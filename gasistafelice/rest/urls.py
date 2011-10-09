 
# Copyright (C) 2011 REES Marche <http://www.reesmarche.org>
# taken from SANET - Laboratori Guglielmo Marconi S.p.A. <http://www.labs.it>
#
# This file is part of GASISTA FELICE
# GASISTA FELICE is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License
#
# GASISTA FELICE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with GASISTA FELICE. If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls.defaults import *

# Entry point for SANET url identification
urlpatterns = patterns('',

    # Welcome page
    (r'^$',                                  'rest.views.index'),
    
    (r'^hh_mm',                               'rest.views.hh_mm'),
    (r'^now',                                 'rest.views.now'),

    (r'^user_roles$',                         'rest.views.user_roles'),
    (r'^switch_role$',                        'rest.views.switch_role'),

    ### FUTURE TODO: these views do not follow the standard URL pattern 
    ### bind them to a site, or move them to another global application
    ### used to perform operation on the whole installation (even if it is multi-site)

    (r'^site_settings$',                     'rest.views.site_settings'),

    # Global methods
    (r'^quick_search/$',                     'rest.views.quick_search'),

    # Global methods
    (r'^list_comments',                      'rest.views.list_comments'),
    (r'^list_notifications',                      'rest.views.list_notifications'),

    (r'^blocks/(?P<resource_type>\w+)/$'                     , 'rest.views.list'),  
    (r'^blocks/(?P<resource_type>\w+)/(?P<resource_id>\d+)/$', 'rest.views.parts'), 
    # END FUTURE TODO

    # Generic
    (r'^(?P<resource_type>\w+)/(?P<resource_id>\d+)/', include('rest.views.urls')), 

    #TODO fero CHECK: the following is needed anymore? ... maybe for permalink or 'natural keys'?
    #TODO (r'^(?P<resource_type>\w+)/(?P<resource_id>\w+)/', include('rest.views.urls')), 

)
