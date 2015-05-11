"""View for block details specialized for a GASSupplierOrder"""

from django.utils.translation import ugettext as ug, ugettext_lazy as _
from django.http import HttpResponse
from django.db import transaction

from flexi_auth.models import ObjectWithContext

from lib.shortcuts import render_to_xml_response
from consts import CASH, INCOME, VIEW_CONFIDENTIAL, CONFIDENTIAL_VERBOSE_HTML
from rest.views.blocks.base import ResourceBlockAction
from rest.views.blocks import AbstractBlock
from gf.gas.forms.cash import BalanceForm, TransationGMForm

import logging
log = logging.getLogger(__name__)

class Block(AbstractBlock):

    BLOCK_NAME = "balance_gm"
    BLOCK_VALID_RESOURCE_TYPES = ["gasmember"]
    BLOCK_DESCRIPTION = ug("Balance")

    def _get_user_actions(self, request):

        user_actions = []
        gas_list = self.resource.gas_list
        for gas in gas_list:
            if request.user.has_perm(CASH, obj=ObjectWithContext(gas)):
                user_actions += [
                    ResourceBlockAction(
                        block_name = self.BLOCK_NAME,
                        resource = self.resource,
                        name=INCOME, verbose_name=ug("Account transaction"),
                        popup_form=False,
                    ),
                ]
                break
        return user_actions

    def get_response(self, request, resource_type, resource_id, args):
        super(Block, self).get_response(request, resource_type, resource_id, args)
        res = self.resource
        gas = res.gas
        extra_html = ""
        if args == "INCOME":
            if request.method == 'POST':
                if request.user.has_perm(CASH, obj=ObjectWithContext(gas)):
                    form = TransationGMForm(request, request.POST)
                    if form.is_valid():
                        with transaction.atomic():
                            if form.cleaned_data:
                                try:

                                    form.save()

                                except Exception, e:
                                    msg = ug("Transaction gasmember ERROR: ") + e.message
                                    form._errors["amount"] = form.error_class([msg])

        else:
            if request.user.has_perm(CASH, obj=ObjectWithContext(gas)):
                form = TransationGMForm(request)
            elif request.user.has_perm(
                VIEW_CONFIDENTIAL, obj=ObjectWithContext(res)
            ): 
                form = BalanceForm(request)
            else:
                form = None
                extra_html = CONFIDENTIAL_VERBOSE_HTML

        ctx = {
            'resource'      : res,
            'sanet_urn'     : "%s/%s" % (resource_type, resource_id),
            'form'          : form,
            'user_actions'  : self._get_user_actions(request),
            'extra_html' : extra_html,
        }
        return render_to_xml_response('blocks/balance_gm.xml', ctx)
