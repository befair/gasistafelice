 
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
from django.http import Http404

from lib.middleware import AppMiddleware
from django.http import HttpResponse

from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings

from gasistafelice.globals import type_model_d
from gasistafelice.gas.models import GASMember

from django.contrib.sessions.backends.db import SessionStore
from django.utils.dateformat import format
import datetime

def get_resource_by_path(resource_type, resource_id):
    # Valid path is: .../<resource_type>/<resource_id>/...others params...

    model = type_model_d[resource_type]
    try:
        if resource_type == GASMember.resource_type:
            resource = model.all_objects.get(pk=resource_id)
        else:
            resource = model.objects.get(pk=resource_id)
    except model.DoesNotExist as e:
        raise Http404

    return resource
        
class ResourceMiddleware(AppMiddleware):

    """Process the view and inject the environment in the request object.
    
    Url pattern is /<app_name>/<resource_type>/<resource_id>/<view_binding>/
    
    """

    def __init__(self):

        super(ResourceMiddleware, self).__init__()

        self.app_settings.update({
            # add here application settings.
        })

    def process_view(self, request, view_func, view_args, view_kwargs):

        kw = view_kwargs
        
        #Special behaviour for RSS Feeds
        if kw.has_key('url'):
            
            path = kw['url'].split('/')[1:] #The first fields is the feed name
            
            kw = {
                'resource_type' : path[0],
                'resource_id' : path[1],
            }
            
        if kw.has_key('resource_type') and kw.has_key('resource_id'):
            request.resource = get_resource_by_path(kw['resource_type'], kw['resource_id'])
                
        return 


class UpdateRequestUserMiddleware(object):

    def process_request(self, request):

        """
        If there is a logged user in the request (i.e: request.user is set),
        update request.user with the User specified in 
        'user_to_simulate' session key
        if the original user has permission to do that
        """
        request.logged_user = request.user

        if request.user and not \
            isinstance(request.user, AnonymousUser):

            if request.session.get('user_to_simulate'):
                request.user = User.objects.get(pk=request.session['user_to_simulate'])

            request.session['logged_user_id'] = request.logged_user.pk
            request.session['user_id'] = request.user.pk

        return 
