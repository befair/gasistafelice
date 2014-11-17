"""View for block insolute management for a GASSupplierOrder"""

from django.utils.translation import ugettext as ug, ugettext_lazy as _
from django.http import HttpResponse
from django.db import transaction

from flexi_auth.models import ObjectWithContext

from lib.shortcuts import render_to_xml_response
from consts import CASH, INCOME
from rest.views.blocks.base import ResourceBlockAction
from rest.views.blocks import AbstractBlock
from app_gas.forms.cash import InsoluteOrderForm

import logging
log = logging.getLogger(__name__)

class Block(AbstractBlock):

    BLOCK_NAME = "order_insolute"
    BLOCK_VALID_RESOURCE_TYPES = ["order"]
    BLOCK_DESCRIPTION = ug("Insolute management")
#    def __init__(self):
#        super(Block, self).__init__()
#        self.description = ug("Insolute management")

    def _get_user_actions(self, request):

        user_actions = []
        order = self.resource.order

        if request.user.has_perm(CASH, obj=ObjectWithContext(self.resource.gas)):

            if order.is_closed() or order.is_unpaid():

                user_actions += [
                    ResourceBlockAction(
                        block_name = self.BLOCK_NAME,
                        resource = self.resource,
                        name=INCOME, verbose_name=ug("Insolute payment"),
                        popup_form=False,
                    ),
                ]

        return user_actions

    def get_response(self, request, resource_type, resource_id, args):

        super(Block, self).get_response(request, resource_type, resource_id, args)

        res = self.resource

        if args == "INCOME":
            if request.method == 'POST':
                form = InsoluteOrderForm(request, request.POST)
                if form.is_valid():
                    with transaction.commit_on_success():
                        if form.cleaned_data:
                            try:

                                form.save()
#                                return self.response_success()
#                                return HttpResponse(_("Insolute saved"))

                            except Exception, e:
                                msg = ug("Transaction Insolute ERROR: ") + e.message
                                form._errors["amount"] = form.error_class([msg])

        else:
            form = InsoluteOrderForm(request)

        ctx = {
            'resource'      : res,
            'sanet_urn'     : "%s/%s" % (resource_type, resource_id),
            'form'          : form,
            'user_actions'  : self._get_user_actions(request),
        }
        return render_to_xml_response('blocks/order_insolute.xml', ctx)
