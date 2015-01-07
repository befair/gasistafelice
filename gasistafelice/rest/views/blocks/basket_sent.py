from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from flexi_auth.models import ObjectWithContext

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response
from gasistafelice.lib.http import HttpResponse

from gasistafelice.gas.models import GASMember

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import cgi, os
from django.conf import settings
from datetime import datetime
import logging
log = logging.getLogger(__name__)
#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "basket_sent"
    BLOCK_DESCRIPTION = _("Basket to deliver")
    BLOCK_VALID_RESOURCE_TYPES = ["gasmember"]

    COLUMN_INDEX_NAME_MAP = {
        0: 'ordered_product__order__pk',
        1: 'ordered_product__gasstock__stock__supplier__name',
        2: 'ordered_product__gasstock__stock__product__name',
        3: 'ordered_price',
        4: 'ordered_amount',
        5: ''
    }

#        5: 'tot_price',

    def _get_resource_list(self, request):
        qs = request.resource.basket_to_be_delivered
        return qs

