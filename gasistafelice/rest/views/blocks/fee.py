from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction, CREATE_PDF

from gasistafelice.lib.shortcuts import render_to_xml_response, render_to_context_response

from gasistafelice.gas.models import GASMember
from gasistafelice.gas.forms.cash import EcoGASMemberFeeFormSet

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import cgi, os
from django.conf import settings

from gasistafelice.consts import CASH, VIEW, EDIT_MULTIPLE
from flexi_auth.models import ObjectWithContext

import logging
log = logging.getLogger(__name__)

from datetime import tzinfo, timedelta, datetime

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "fee"
    BLOCK_DESCRIPTION = _("Fee gasmember")
    BLOCK_VALID_RESOURCE_TYPES = ["gas"]

    COLUMN_INDEX_NAME_MAP = {
        0: 'id',
        1: 'person__surname',
        2: '',
        3: ''
    }
#        2: 'last_fee',

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
        return EcoGASMemberFeeFormSet

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        data = {}
#       c = querySet.count()

        map_info = { }

        i = 0
        actual_year = datetime.now().strftime('%Y')
        for i, item in enumerate(querySet):

            key_prefix = 'form-%d' % i

            log.debug("Fee enumerate (%s) - %s" % (i, item))

            data.update({
               '%s-gm_id' % key_prefix : item.pk,
               '%s-feeed' % key_prefix : 0,
               '%s-year' % key_prefix : '0', #actual_year,
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
               'last_fee' : item.last_fee,
               'yearing' : "%s" % (form['year']),
               'feeing' : "%s %s" % (form['gm_id'], form['feeed']),
            })

        return formset, records, {}


