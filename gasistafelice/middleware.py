 
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

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.shortcuts import get_object_or_404

from lib.middleware import AppMiddleware
from django.http import HttpResponse

from django.conf import settings

from gasistafelice.des.models import type_model_d

class URNMiddleware(AppMiddleware):
	"""Process the view and inject the environment in the request object.
    
    Url pattern is /<resource_type>/<resource_id>/<app_name>/<view_binding> 
	
    """
    #TODO fero: CHECK url pattern

	def __init__(self):

		super(URNMiddleware, self).__init__()

		self.app_settings.update({
			# add here application settings.
		})

	def __get_resource_by_path(self, request, **kw):
		# Valid path is: .../<resource_type>/<resource_id>/...others params...
		
		try:
			resource_type = kw['resource_type']
			resource_id   = kw['resource_id']
			
			model = type_model_d[resource_type]
			
			return get_object_or_404(model, pk=resource_id)
		except KeyError, k:
			#raise ValueError(_("URL does not identify a GASISTA FELICE resource"))
			pass
			
		#return get_object_or_404(model, pk=resource_id)
		return None
		
	def process_view(self, request, view_func, view_args, view_kwargs):

		kw = view_kwargs
		
		if kw.has_key('url'):
			
			#RSS Feeds
			path = kw['url'].split('/')[1:] #The first fields is the feed name
			
			kw = {
				'resource_type' : path[0],
				'resource_id' : path[1],
			}
			
		if kw.has_key('resource_type') and kw.has_key('resource_id'):
			
			if kw['resource_type'] != 'blocks':
			
				request.resource = self.__get_resource_by_path(request, **kw)
				
		return 

