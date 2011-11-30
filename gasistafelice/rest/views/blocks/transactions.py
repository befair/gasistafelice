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
        0: 'pk',
        1: 'date',
        2: 'issuer',
        3: 'source',
        4: 'kind',
        5: 'description',
        6: 'is_confirmed'
    }
#Transaction
#    date = models.DateTimeField(default=datetime.now)
#    description = models.CharField(max_length=512, help_text=_("Reason of the transaction"))
#    issuer = models.ForeignKey(Subject, related_name='issued_transactions_set')
#    source = models.ForeignKey(CashFlow)     
#    split_set = models.ManyToManyField(Split)
#    kind = models.CharField(max_length=128, choices=settings.TRANSACTION_TYPES)
#    is_confirmed = models.BooleanField(default=False)
#    def splits(self):
#    def is_split(self):
#    def is_internal(self):
#    def is_simple(self):

#LedgerEntry
#    account = models.ForeignKey(Account, related_name='entry_set')
#    transaction = models.ForeignKey(Transaction, related_name='entry_set')
#    entry_id = models.PositiveIntegerField(null=True, blank=True, editable=False)
#    amount = CurrencyField()
#    def date(self):
#    def description(self):
#    def issuer(self):

#TODO: Desired column
#        1: 'pk',
#        2: 'date',
#        3: 'Entrata',  --> Amount
#        4: 'Uscita'  --> Amount
#        5: 'Type',  --> Transaction type
#        6: 'description'


    def _get_resource_list(self, request):
        #Accounting.LedgerEntry  or Transactions
        return request.resource.transactions

