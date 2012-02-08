from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables


#from simple_accounting.models import economic_subject, AccountingDescriptor
#from simple_accounting.models import account_type
#from simple_accounting.exceptions import MalformedTransaction
#from simple_accounting.models import AccountingProxy
#from simple_accounting.utils import register_transaction, register_simple_transaction

#from gasistafelice.base.accounting import PersonAccountingProxy

from gasistafelice.lib.shortcuts import render_to_xml_response, render_to_context_response

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "transactions"
    BLOCK_DESCRIPTION = _("Economic transactions")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas", "supplier", "pact", "gasmember"]

    COLUMN_INDEX_NAME_MAP = {
        0: 'id',
        1: 'transaction__date',
        2: '',
        3: '',
        4: 'amount',
        5: 'transaction__description',
    }

#WAS        2: 'transaction__issuer',
#WAS        3: 'transaction__source',
#WAS        4: 'transaction__kind',

    def _get_resource_list(self, request):
        #Accounting.LedgerEntry  or Transactions
        return request.resource.economic_movements

#TODO: Filter grid by
# Date From --> To
# Kind iof transctions: can be checkbox list multiselect
# Subject: Radio or multiple checkbox onto values [GAS borselino, GASMemmbers, Suppliers]
#    def options_response(self, request, resource_type, resource_id):
#        """Get options for transaction block. 
#        WARNING: call to this method doesn't pass through get_response
#        so you have to reset self.request and self.resource attribute if you want
#        """
#        self.request = request
#        self.resource = request.resource
#        fields = []
#        #DATE FROM
#        fields.append({
#            'field_type'   : 'datetime',
#            'field_label'  : 'from date',
#            'field_name'   : 'from',
#            'field_values' : [{ 'value' : '22/09/2012', 'selected' : ''}]
#        })
#        #DATE TO
#        fields.append({
#            'field_type'   : 'datetime',
#            'field_label'  : 'to date',
#            'field_name'   : 'to',
#            'field_values' : [{ 'value' : '28/09/2012', 'label' : 'labelvalue', 'selected' : 'sel'}]
#        })
#        ctx = {
#            'block_name' : self.description,
#            'fields': fields,
#        }
#        #Can use html template loader
#        return render_to_xml_response('eco-options.xml', ctx)

