 
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
	
	(r'hh_mm',                               'rest.views.hh_mm'),

	(r'^site_settings$',                     'rest.views.site_settings'),

	# Global methods
	(r'^quick_search/$',                     'rest.views.quick_search'),

	# Global methods
	(r'^list_comments',                      'rest.views.list_comments'),

	#List of specific resources needed?
    #OLD (r'^list_nodes$',                        'rest.views.list_nodes'), # Get list of nodes          

	#
	(r'^blocks/(?P<resource_type>\w+)/$'                     , 'rest.views.list'),  
	(r'^blocks/(?P<resource_type>\w+)/(?P<resource_id>\d+)/$', 'rest.views.parts'), 

	# Generic
	(r'^(?P<resource_type>\w+)/(?P<resource_id>\d+)/', include('rest.views.urls')), 
	(r'^(?P<resource_type>\w+)/(?P<resource_id>\w+)/', include('rest.views.urls')), 

)
