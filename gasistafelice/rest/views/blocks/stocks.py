from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction
from gasistafelice.auth import CREATE, EDIT

from gasistafelice.supplier.models import Supplier

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "stocks"
    BLOCK_DESCRIPTION = _("Stocks")
    BLOCK_VALID_RESOURCE_TYPES = ["supplier"] 

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(EDIT, obj=Supplier):
            user_actions.append( 
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=EDIT, verbose_name=_("Edit stock"), 
                )
            )

        return user_actions
        
    def _get_resource_list(self, request):
        return request.resource.stocks

