"""View for block details specialized for a GASSupplierOrder"""

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.http import HttpResponse

from flexi_auth.models import ObjectWithContext

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response
from gasistafelice.rest.views.blocks import details
from gasistafelice.gas.forms import cash as order_cash_forms

from gasistafelice.consts import CASH, VIEW, EDIT_MULTIPLE, INCOME
from gasistafelice.rest.views.blocks.base import ResourceBlockAction
from gasistafelice.rest.views.blocks import AbstractBlock
from gasistafelice.gas.forms.cash import CashOrderForm

import logging
log = logging.getLogger(__name__)

class Block(AbstractBlock):

    BLOCK_NAME = "order_invoice"
    BLOCK_VALID_RESOURCE_TYPES = ["order"]

    def __init__(self):
        super(Block, self).__init__()
        self.description = _("Invoice management")

    def _get_user_actions(self, request):

        user_actions = []
        if request.user.has_perm(CASH, obj=ObjectWithContext(self.resource.gas)):

            user_actions += [
                ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = self.resource,
                    name=INCOME, verbose_name=_("Invoice receipt"),
                    popup_form=False,
                ),
            ]

        return user_actions

    def get_response(self, request, resource_type, resource_id, args):

        super(Block, self).get_response(request, resource_type, resource_id, args)

        res = self.resource

        user_actions = self._get_user_actions(request)
        if args == "":
            ctx = {
                'resource'      : res,
                'sanet_urn'     : "%s/%s" % (resource_type, resource_id),
                'form'          : CashOrderForm(request),
                'user_actions'  : user_actions,
            }
            return render_to_xml_response('blocks/order_invoice.xml', ctx)
        elif args == "INCOME":
            if request.method == 'POST':

                form = CashOrderForm(request, request.POST)

                if form.is_valid():
                    with transaction.commit_on_success():
                        if form.cleaned_data:
                            form.save()
                    return self.response_success()
                else:
                    return self.response_error(form.errors)


        
#    def _get_edit_form_class(self):
#        # TODO:  TOVERIFY fero
#        """GASSupplierOrder is an atom, so we have to return a formset"""
#        #return order_cash_forms.form_class_factory_for_request(self.request, base=order_forms.CashOrderForm)
#        return order_cash_forms.CashOrderForm()

#    def get_description(self):
#        return _("%(name)s's GAS memberships") % {
#            'name' : self.resource.order.report_name,
#        }

#DOMTHU
#    def total_amount(self):
#    def tot_price(self):
#    def tot_amount(self):
#    def tot_gasmembers(self):
#    def tot_curtail(self):
#    def payment(self):
#    def payment_urn(self):


#state
#tot_price 1
#invoice_amount 2 
#payment 3

#invoice_note

#unsolved Multiplechoice 
#total 1 2 3  (ordinati + fatture + pagati)

#amount_to_pay textbox


