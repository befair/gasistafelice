 
# Copyright (C) 2008 Laboratori Guglielmo Marconi S.p.A. <http://www.labs.it>
#
# This file is part of SANET
# SANET is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License
#
# SANET is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with SANET. If not, see <http://www.gnu.org/licenses/>.

from django.http import HttpResponse
from django.conf import settings

class AppMiddleware(object):
    """Process the view and inject the environment in the request object"""
    
    def __init__(self):

        self.app_settings = {
            'theme' : getattr(settings, 'THEME_NAME', ''),
            'VERSION' : getattr(settings, 'VERSION', '0.1'),
        }

    def process_request(self, request):
        """Fill request with the `app_settings` attribute to store 
        user profile settings"""

        user_settings = request.session.get('app_settings', {})

        if not user_settings:

            #TODO: Persistent user settings 
            request.session['app_settings'] = self.app_settings

        elif user_settings.get('VERSION') != self.app_settings['VERSION']:

            # Get default settings of the new version 
            request.session['app_settings'] = self.app_settings
            # DISABLED BECAUSE OF NO RETROCOMPATIBILITY WITH previous settings.
            # ... and then update them with the user preferences
            # NOTE: assume there is retrocompatibility among new and old settings
            # user_settings.pop('VERSION',None)
            # request.session['app_settings'].update(user_settings)


        # Put settings in the request
        request.app_settings = request.session['app_settings']

        # Always add DEBUG symbol
        request.app_settings['DEBUG'] = settings.DEBUG

        return 
