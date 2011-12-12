from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables


#from simple_accounting.models import economic_subject, AccountingDescriptor
#from simple_accounting.models import account_type
#from simple_accounting.exceptions import MalformedTransaction
#from simple_accounting.models import AccountingProxy
#from simple_accounting.utils import register_transaction, register_simple_transaction

#from gasistafelice.base.accounting import PersonAccountingProxy



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
        2: 'transaction__issuer',
        3: 'transaction__source',
        4: 'transaction__kind',
        5: 'transaction__description',
        6: '',
    }
#        6: 'is_confirmed'
#Cannot resolve keyword 'issuer' into field. Choices are: account, amount, entry_id, id, transaction




    def _get_resource_list(self, request):
        #Accounting.LedgerEntry  or Transactions
        return request.resource.economic_movements


#        "{{entry.account.name|escapejs}}",
#        "{{entry.urn|escapejs}}",
#        "{{entry.transaction.kind|escapejs}}",


