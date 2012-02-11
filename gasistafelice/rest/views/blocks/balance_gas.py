"""View for block details specialized for a GASSupplierOrder"""

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.http import HttpResponse
from django.db import transaction

from flexi_auth.models import ObjectWithContext

from gasistafelice.lib.shortcuts import render_to_xml_response
from gasistafelice.rest.views.blocks import details

from gasistafelice.consts import CASH, INCOME
from gasistafelice.rest.views.blocks.base import ResourceBlockAction
from gasistafelice.rest.views.blocks import AbstractBlock
from gasistafelice.gas.forms.cash import BalanceGASForm, TransationGASForm

import logging
log = logging.getLogger(__name__)

class Block(AbstractBlock):

    BLOCK_NAME = "balance_gas"
    BLOCK_VALID_RESOURCE_TYPES = ["gas"]
    BLOCK_DESCRIPTION = _("Balance")
#    def __init__(self):
#        super(Block, self).__init__()
#        self.description = _("Balance")

    def _get_user_actions(self, request):

#COMMENT BY fero: no need for these actions now
        user_actions = []
        gas_list = self.resource.gas_list
        for gas in gas_list:
            if request.user.has_perm(CASH, obj=ObjectWithContext(gas)):
                user_actions += [
                    ResourceBlockAction(
                        block_name = self.BLOCK_NAME,
                        resource = self.resource,
                        name=INCOME, verbose_name=_("Account transaction"),
                        popup_form=False,
                    ),
                ]
                break
        return user_actions

    def get_response(self, request, resource_type, resource_id, args):
        super(Block, self).get_response(request, resource_type, resource_id, args)
        res = self.resource
        #TODO-not-a-priority domthu: show as popup
        gas = res.gas
        if args == "INCOME":
            if request.method == 'POST':
                if request.user.has_perm(CASH, obj=ObjectWithContext(gas)):
                    form = TransationGASForm(request, request.POST)
                else:
                    form = BalanceGASForm(request, request.POST)
                if form.is_valid():
                    with transaction.commit_on_success():
                        if form.cleaned_data:
                            try:

                                form.save()
#                                return self.response_success()

                            except ValueError, e:
                                msg = _("Transaction invoice ERROR: ") + e.message
                                #WAS return self.response_error(form.errors)
                                #WAS form._errors.append(msg)
                                #WAS form.ValidationError(_(msg))
                                form._errors["amount"] = form.error_class([msg])

#WAS: forms errors not rendered --> DO NOTHING render ctx for showing errors
# return self.response_error(form.errors)

        else:
            if request.user.has_perm(CASH, obj=ObjectWithContext(gas)):
                form = TransationGASForm(request)
            else:
                form = BalanceGASForm(request)

        ctx = {
            'resource'      : res,
            'sanet_urn'     : "%s/%s" % (resource_type, resource_id),
            'form'          : form,
            'user_actions'  : self._get_user_actions(request),
        }
        return render_to_xml_response('blocks/balance_gas.xml', ctx)
