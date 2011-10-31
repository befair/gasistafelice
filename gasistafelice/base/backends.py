# Copyright (C) 2011 REES Marche <http://www.reesmarche.org>
#
# This file is part of ``gasistafelice``.

# ``gasistafelice`` is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# ``gasistafelice`` is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with ``gasistafelice``. If not, see <http://www.gnu.org/licenses/>.

from flexi_auth.exceptions import WrongPermissionCheck
from flexi_auth.models import PrincipalParamRoleRelation
from django.contrib.auth.backends import ModelBackend

class AuthenticationParamRoleBackend(ModelBackend):
    """
    Django authentication backend to state that a User with no role cannot log in
    """
    
    def authenticate(self, username, password):
        """
        This is an authenticate-only backend, so it's good to be here! ;)
        """
        
        rv = user = super(AuthenticationParamRoleBackend, self).authenticate(username, password)

        if not PrincipalParamRoleRelation.objects.filter(user=user).count():
            rv = None
       
        return rv
        
