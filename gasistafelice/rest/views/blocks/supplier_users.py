
from gasistafelice.rest.views.blocks import users 

from flexi_auth.models import ParamRole
from gasistafelice.consts import SUPPLIER_REFERRER

from registration.models import RegistrationProfile

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(users.Block):

    BLOCK_NAME = "supplier_users"
    BLOCK_VALID_RESOURCE_TYPES = ["supplier"]

    def _get_resource_list(self, request):
        """Rather than adding a 'users' method to the resource,
        we compute users list here, because users may be not still bound to
        the correspondent Person. This block is in fact used only for Admin
        purposes during a specific stage of the registration process.
        """
        # User list
        pr = ParamRole.get_role(SUPPLIER_REFERRER, supplier=request.resource)
        users = pr.get_users()
        users = users.filter(registrationprofile__activation_key=RegistrationProfile.ACTIVATED)
        return users.order_by('last_name', 'first_name')
