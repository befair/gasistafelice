"""View for block details specialized for a GASSupplierOrder"""

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.http import HttpResponse
from django.db import transaction

from flexi_auth.models import ObjectWithContext

from lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response
from rest.views.blocks import details
from gf.gas.forms import cash as order_cash_forms

from consts import CASH, VIEW, EDIT_MULTIPLE, INCOME
from rest.views.blocks.base import ResourceBlockAction
from rest.views.blocks import AbstractBlock
from gf.gas.forms.cash import InvoiceOrderForm

from django.conf import settings

import logging
log = logging.getLogger(__name__)

class Block(AbstractBlock):

    BLOCK_NAME = "order_invoice"
    BLOCK_VALID_RESOURCE_TYPES = ["order"]

    def __init__(self):
        super(Block, self).__init__()
        self.description = _("Actual total registration")

    def _get_user_actions(self, request):

        user_actions = []
        order = self.resource.order

        if request.user.has_perm(CASH, obj=ObjectWithContext(order.gas)) or \
            request.user == order.referrer_person.user:

            if order.is_closed() or order.is_unpaid():

                user_actions += [
                    ResourceBlockAction(
                        block_name = self.BLOCK_NAME,
                        resource = self.resource,
                        name=INCOME, verbose_name=_("Register"),
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
                    with transaction.atomic():
                        if form.cleaned_data:
                            try:

                                form.save()
#                                return self.response_success()

                            except Exception, e:
                                if settings.FORM_DEBUG:
                                    raise
                                else:
                                    msg = _("Error in invoice registration: ") + e.message
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

