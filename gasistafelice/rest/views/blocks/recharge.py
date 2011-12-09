from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction, CREATE_PDF
from gasistafelice.consts import CREATE, EDIT, EDIT_MULTIPLE, VIEW

from gasistafelice.lib.shortcuts import render_to_xml_response, render_to_context_response

from gasistafelice.gas.models import GASMember, GASMemberOrder
from gasistafelice.supplier.models import Supplier
from gasistafelice.gas.forms.cash import EcoGASMemberRechargeForm, BaseFormSetWithRequest, formset_factory

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import cgi, os
from django.conf import settings

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
        0: 'pk', 
        1: 'gasmember',
        2: 'last_recharge',
        3: ''
    }

    def _get_user_actions(self, request):
  
        user_actions = []

        #FIXME: Check if order is in "closed_state"  Not in Open STATE for CASH REFERRER
        #if request.user.has_perm(CASH, obj=ObjectWithContext(request.resource)):
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
        return gas.gasmembers

    def _get_edit_multiple_form_class(self):
        return formset_factory(
            form=EcoGASMemberRechargeForm,
            formset=BaseFormSetWithRequest,
            extra=0
        )

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

            records.append({
               'id' : item.pk,
               'gasmember' : item,
               'last_recharge' : item.last_recharge,
               'recharging' : "%s %s" % (form['gm_id'], form['recharged']),
            })

        return formset, records, {}

