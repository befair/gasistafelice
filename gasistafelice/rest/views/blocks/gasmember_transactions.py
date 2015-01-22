
from rest.views.blocks import transactions

class Block(transactions.Block):

    BLOCK_NAME = "gasmember_transactions"
    BLOCK_VALID_RESOURCE_TYPES = ["gasmember"] 

    def _check_permission(self):

        return self.request.user.has_perm(
            VIEW_CONFIDENTIAL, 
            obj=ObjectWithContext(self.request.resource)
        ) or self.request.user.has_perm(
            CASH, 
            obj=ObjectWithContext(self.request.resource.gas)
        )

    def get_response(self, request, resource_type, resource_id, args):
        if not self._check_permission():

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

        if not self._check_permission():
            rv = []
        else:
            rv = super(Block, self)._get_user_actions(request)

        return rv

