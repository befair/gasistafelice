"""View for economic block specialized for a GASSupplierSolidalPact and GASSupplierOrder"""

from django.utils.translation import ugettext, ugettext_lazy as _
from django.http import HttpResponse
from django.db import transaction

from flexi_auth.models import ObjectWithContext

from gasistafelice.lib.shortcuts import render_to_xml_response
from gasistafelice.consts import CASH, INCOME
from gasistafelice.rest.views.blocks.base import ResourceBlockAction
from gasistafelice.rest.views.blocks import AbstractBlock
from gasistafelice.gas.forms.cash import BalanceForm, TransationPACTForm

import logging
log = logging.getLogger(__name__)

class Block(AbstractBlock):

    BLOCK_NAME = "balance_pact"
    BLOCK_VALID_RESOURCE_TYPES = ["pact"]
    BLOCK_DESCRIPTION = ugettext("Balance")

    def _get_user_actions(self, request):

        user_actions = []
        gas_list = self.resource.gas.gas_list

        pact = self.resource

        for gas in gas_list:
            #Pact referrers can make economic transactions BUT cannot do economic corrections
            if request.user.has_perm(CASH, obj=ObjectWithContext(gas)) or request.user in pact.referrers:
                user_actions += [
                    ResourceBlockAction(
                        block_name = self.BLOCK_NAME,
                        resource = pact,
                        name=INCOME, verbose_name=ugettext("Account transaction"),
                        popup_form=False,
                    ),
                ]
                break
        return user_actions

    def get_response(self, request, resource_type, resource_id, args):
        super(Block, self).get_response(request, resource_type, resource_id, args)
        res = self.resource
        gas = res.gas
        if args == "INCOME":
            if request.method == 'POST':
                if request.user.has_perm(CASH, obj=ObjectWithContext(gas)):
                    form = TransationPACTForm(request, request.POST)
                    if form.is_valid():
                        with transaction.commit_on_success():
                            if form.cleaned_data:
                                try:

                                    form.save()

                                except Exception, e:
                                    msg = ugettext("Transaction pact ERROR: ") + e.message
                                    form._errors["amount"] = form.error_class([msg])

        else:
            if request.user.has_perm(CASH, obj=ObjectWithContext(gas)):
                form = TransationPACTForm(request)
            else:
                form = BalanceForm(request)

        ctx = {
            'resource'      : res,
            'sanet_urn'     : "%s/%s" % (resource_type, resource_id),
            'form'          : form,
            'user_actions'  : self._get_user_actions(request),
        }
        return render_to_xml_response('blocks/balance_pact.xml', ctx)
