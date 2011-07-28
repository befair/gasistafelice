from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockWithList, Action
from gasistafelice.auth import CREATE

from gasistafelice.supplier.models import SupplierStock

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "stocks"
    BLOCK_DESCRIPTION = _("Stocks")
    BLOCK_VALID_RESOURCE_TYPES = ["supplier"] 

    TEMPLATE_RESOURCE_LIST_WITH_DETAILS = 'blocks/stocks_with_details.xml'

    # Actions
    ACTION_CREATE = Action(
        name=CREATE, 
        verbose_name=_("Add product"), 
        url=urlresolvers.reverse('admin:gas_gas_add')
    )

    def _get_user_actions(self, request):

        user_actions = []
        if request.user.has_perm(CREATE, obj=SupplierStock):
            user_actions.append(self.ACTION_CREATE)

        return user_actions
        

    def _get_resource_list(self, request):
        return request.resource.stocks

