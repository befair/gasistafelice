"""View for block details specialized for a GASSupplierOrder"""

from django.utils.translation import ugettext as ug, ugettext_lazy as _
from django.http import HttpResponse
from django.db import transaction

from flexi_auth.models import ObjectWithContext

from lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response
from rest.views.blocks import details
from gf.gas.forms import cash as order_cash_forms

from consts import CASH, VIEW, EDIT_MULTIPLE, INCOME
from rest.views.blocks.base import ResourceBlockAction
from rest.views.blocks import AbstractBlock
from gf.gas.forms.cash import BalanceForm

import logging
log = logging.getLogger(__name__)

class Block(AbstractBlock):

    BLOCK_NAME = "balance"
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas", "supplier", "pact", "gasmember"]
    BLOCK_DESCRIPTION = ug("Balance")

    def _get_user_actions(self, request):
        #COMMENT BY fero: no need for these actions now
        return []

        user_actions = []
        gas_list = self.resource.gas_list

        for gas in gas_list:
            if request.user.has_perm(CASH, obj=ObjectWithContext(gas)):

                user_actions += [
                    ResourceBlockAction(
                        block_name = self.BLOCK_NAME,
                        resource = self.resource,
                        name=INCOME, verbose_name=ug("Balance state"),
                        popup_form=False,
                    ),
                ]
                break

        return user_actions

    def get_response(self, request, resource_type, resource_id, args):

        super(Block, self).get_response(request, resource_type, resource_id, args)

        res = self.resource

        user_actions = self._get_user_actions(request)
        if args == "INCOME":
            if request.method == 'POST':

                form = BalanceForm(request, request.POST)

                if form.is_valid():
                    with transaction.atomic():
                        if form.cleaned_data:
                            form.save()
#                    return self.response_success()
#                else:
#                    return self.response_error(form.errors)

        else:
                form = BalanceForm(request)

#        if args == "":
        ctx = {
            'resource'      : res,
            'sanet_urn'     : "%s/%s" % (resource_type, resource_id),
            'form'          : BalanceForm(request),
            'user_actions'  : user_actions,
        }
        return render_to_xml_response('blocks/balance.xml', ctx)


#class Block(InfoBlock):
#
#    BLOCK_NAME = "balance"
#    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas", "supplier", "pact", "gasmember"]
#    BLOCK_DESCRIPTION = ug("balance")
#
#    def get_response(self, request, resource_type, resource_id, args):
#
#        super(Block, self).get_response(request, resource_type, resource_id, args)
#
#        if args == "":
#            return self.render_details_block(request, resource_type, resource_id)
