# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction, CREATE_PDF

from gasistafelice.lib.shortcuts import render_to_xml_response, render_to_context_response

from gasistafelice.gas.models import GASMember
from gasistafelice.gas.forms.cash import EcoGASMemberRechargeFormSet

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

from gasistafelice.consts import CASH, VIEW, EDIT_MULTIPLE
from gasistafelice.consts import VIEW_CONFIDENTIAL, CONFIDENTIAL_VERBOSE_HTML
from flexi_auth.models import ObjectWithContext

import logging
log = logging.getLogger(__name__)

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "recharge"
    BLOCK_DESCRIPTION = _("Recharge gasmember")
    BLOCK_VALID_RESOURCE_TYPES = ["gas"]

    COLUMN_INDEX_NAME_MAP = {
        0: 'id',
        1: 'person__surname',
        2: '',
        3: '',
        4: 'person__name'
    }
#        2: 'last_recharge',

    def __init__(self, *args, **kw):
        
        super(Block, self).__init__(*args, **kw)
        
        # Default start closed. Mainly for GAS -> Accounting tab ("Conto")
        self.start_open   = False

    def _get_user_actions(self, request):
  
        user_actions = []

        gas = request.resource.gas

        if request.user.has_perm(CASH, obj=ObjectWithContext(gas)):

            user_actions += [
                ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=VIEW, verbose_name=_("Show"),
                    popup_form=False,
                    method="get",
                ),
                ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=EDIT_MULTIPLE, verbose_name=_("Edit"),
                    popup_form=False,
                    method="get",
                ),
            ]

        return user_actions

    def _get_resource_list(self, request):
        #return GASMember objects
        gas = request.resource.gas
        return gas.gasmembers.order_by('person__surname', 'person__name')

    def _get_edit_multiple_form_class(self):
        return EcoGASMemberRechargeFormSet

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        data = {}
#       c = querySet.count()

        map_info = { }

        i = 0
        for i, item in enumerate(querySet):

            key_prefix = 'form-%d' % i

            log.debug("Recharge enumerate (%s) - %s" % (i, item))

            data.update({
               '%s-gm_id' % key_prefix : item.pk,
               '%s-recharged' % key_prefix : 0,
            })

            map_info[item.pk] = {'formset_index' : i}

        data['form-TOTAL_FORMS'] = i + 1
        data['form-INITIAL_FORMS'] = i + 1
        data['form-MAX_NUM_FORMS'] = 0

        formset = self._get_edit_multiple_form_class()(request, data)

        records = []
        i = 0
        for i,item in enumerate(querySet):

            form = formset[map_info[item.pk]['formset_index']]
            print "item.balanceitem.balanceitem.balanceitem.balance %s" % ("%.2f" % round(item.balance, 2)).replace('.','€')
            records.append({
               'id' : item.pk,
               'gasmember' : item,
               'last_recharge' : item.last_recharge,
               'recharging' : "%s %s" % (form['gm_id'], form['recharged']),
               'gasmember_urn' : item.urn,
               'balance' : ("%.2f" % round(item.balance, 2)).replace('.','€'),
            })

        return formset, records, {}

    def get_response(self, request, resource_type, resource_id, args):
        """Check for confidential access permission and call superclass if needed"""

        if not request.user.has_perm(
                CASH, obj=ObjectWithContext(request.resource.gas)
            ): 

            return render_to_xml_response(
                "blocks/table_html_message.xml", 
                { 'msg' : CONFIDENTIAL_VERBOSE_HTML }
            )

        return super(Block, self).get_response(request, resource_type, resource_id, args)


