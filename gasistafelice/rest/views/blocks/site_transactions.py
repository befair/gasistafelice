
from rest.views.blocks import transactions

from flexi_auth.models import ObjectWithContext

from gasistafelice.consts import CONFIDENTIAL_VERBOSE_HTML, CASH

class Block(transactions.Block):

    BLOCK_NAME = "site_transactions"
    BLOCK_VALID_RESOURCE_TYPES = ["site"] 

    def _check_permission(self, request):

        return request.user in request.resource.gas_tech_referrers | \
                request.resource.gas_cash_referrers

    def _get_user_actions(self, request):

        if not self._check_permission(request):
            rv = []
        else:
            rv = super(Block, self)._get_user_actions(request)

        return rv

