
from rest.views.blocks import transactions

from flexi_auth.models import ObjectWithContext

from lib.shortcuts import render_to_xml_response
from gasistafelice.consts import VIEW_CONFIDENTIAL, CONFIDENTIAL_VERBOSE_HTML, CASH

class Block(transactions.Block):

    BLOCK_NAME = "gasmember_transactions"
    BLOCK_VALID_RESOURCE_TYPES = ["gasmember"]

    def _check_permission(self, request):

        return request.user.has_perm(
            VIEW_CONFIDENTIAL,
            obj=ObjectWithContext(request.resource)
        )
        #WAS: checked in superclass
        #WAS:       or request.user.has_perm(
        #WAS:            CASH,
        #WAS:            obj=ObjectWithContext(request.resource.gas)
        #WAS:        )


    def get_response(self, request, resource_type, resource_id, args):
        if not self._check_permission(request):

            rv = render_to_xml_response(
                "blocks/table_html_message.xml",
                { 'msg' : CONFIDENTIAL_VERBOSE_HTML }
            )

        else:
            rv = super(Block, self).get_response(
                request, resource_type, resource_id, args
            )

        return rv

    def _get_user_actions(self, request):

        if not self._check_permission(request):
            rv = []
        else:
            rv = super(Block, self)._get_user_actions(request)

        return rv

