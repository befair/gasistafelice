
# IMHO this does not work
from django.utils.translation import ugettext_lazy as _
import consts

SUBJECTIVE_MODELS = (
    'gas.GAS',
    'gas.GASMember',
    'supplier.Supplier',                      
)

ACCOUNT_TYPES = (
    (consts.INCOME, _('Incomes')),
    (consts.EXPENSE, _('Expenses')),
    (consts.ASSET, _('Assets')),
    (consts.LIABILITY, _('Liabilities')),
    (consts.EQUITY, _('Equity')),     
)

TRANSACTION_TYPES = (
     (consts.INVOICE_PAYMENT, 'Payment of an invoice '),
     (consts.INVOICE_COLLECTION, 'Collection of an invoice'),
     (consts.GAS_MEMBER_RECHARGE, _('Re-charge from a GAS member')),
     (consts.MEMBERSHIP_FEE_PAYMENT, _('Payment of annual membership fee by a GAS member')),
)


