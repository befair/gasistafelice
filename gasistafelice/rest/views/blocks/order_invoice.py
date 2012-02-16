"""View for block details specialized for a GASSupplierOrder"""

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.http import HttpResponse
from django.db import transaction

from flexi_auth.models import ObjectWithContext

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response
from gasistafelice.rest.views.blocks import details
from gasistafelice.gas.forms import cash as order_cash_forms

from gasistafelice.consts import CASH, VIEW, EDIT_MULTIPLE, INCOME
from gasistafelice.rest.views.blocks.base import ResourceBlockAction
from gasistafelice.rest.views.blocks import AbstractBlock
from gasistafelice.gas.forms.cash import InvoiceOrderForm

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
        order = self.resource.order

        if request.user.has_perm(CASH, obj=ObjectWithContext(order.gas)) or \
            request.user == order.referrer_person.user:

            if order.is_closed():

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
        if args == "INCOME":
            if request.method == 'POST':

                form = InvoiceOrderForm(request, request.POST)

                if form.is_valid():
                    with transaction.commit_on_success():
                        if form.cleaned_data:
                            try:

                                form.save()
#                                return self.response_success()

                            except Exception, e:
                                msg = _("Transaction invoice ERROR: ") + e.message
                                form._errors["amount"] = form.error_class([msg])

        else:
                form = InvoiceOrderForm(request)

        ctx = {
            'resource'      : res,
            'sanet_urn'     : "%s/%s" % (resource_type, resource_id),
            'form'          : form,
            'user_actions'  : user_actions,
        }
        return render_to_xml_response('blocks/order_invoice.xml', ctx)

