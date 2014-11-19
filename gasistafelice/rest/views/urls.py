 
# Copyright (C) 2011 REES Marche <http://www.reesmarche.org>
# taken from SANET by Laboratori Guglielmo Marconi S.p.A. <http://www.labs.it>
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


from django.conf.urls import patterns, include, url

from actions import *

urlpatterns = patterns('rest.views',

    (r'^$',                'resource_page'),
    (r'^related_notes/$',  'related_notes'),

    #TEST (r'^gas_details/manage_roles', 'manage_roles'), # done

    # Suspend a resource (POST)
    #(r'^action/suspend',            suspend_resource),


    # TEST VIEWS FOR THE PROXY AGGREGATOR
    #(r'^withsecret/(?P<view_type>\w+)/$',             'view_factory2'), # done
    #(r'^withsecret/(?P<view_type>\w+)/(?P<args>.+)$',     'view_factory2'), # done


    (r'^(?P<view_type>\w+)/$',             'view_factory'), # done
    (r'^(?P<view_type>\w+)/(?P<args>.+)$', 'view_factory'), # done


)

