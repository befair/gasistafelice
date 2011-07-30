from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockWithList, ResourceBlockAction
from gasistafelice.auth import CREATE

from gasistafelice.supplier.models import Supplier

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "stocks"
    BLOCK_DESCRIPTION = _("Stocks")
    BLOCK_VALID_RESOURCE_TYPES = ["supplier"] 

    TEMPLATE_RESOURCE_LIST_WITH_DETAILS = 'blocks/stocks_with_details.xml'

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

    def get_response(self, request, resource_type, resource_id, args):

        resource = request.resource

        if args == "":

            context = {
                'block_type' : self.name,
                'resource'   : resource,
                'resource_list'   : self._get_resource_list(request),
                'user_actions'    : self._get_user_actions(request),
            }

            if request.GET.get('display') == 'resource_list_with_details':
                template = self.TEMPLATE_RESOURCE_LIST_WITH_DETAILS
            else:
                template = self.TEMPLATE_RESOURCE_LIST
                
            return render_to_xml_response(template, context)

        elif args == CREATE:

            return self._add_resource(request)

        else:
            raise NotImplementedError

