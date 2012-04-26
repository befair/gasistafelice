from django.utils.translation import ugettext_lazy as _

#TODO: to be reviewed and maybe cleaned
TRANSACTION_TYPES_D = {
     'INVOICE_PAYMENT' : _("Payment of an invoice"),
     'INVOICE_COLLECTION' : _("Collection of an invoice"),
     'RECHARGE' : _("Recharge made by a GAS member"),
     'MEMBERSHIP_FEE' : _("Payment of a membership fee by a GAS member"),
     'PAYMENT' : _("A generic payment"),
     'GAS_WITHDRAWAL' : _("A withdrawal from a member's account made by a GAS"),
     'REFUND' : _("A money refund made by a supplier to a GAS"),
     'PACT_EXTRA' : _("An arbitrary money transfer related to a solidal pact"),
     'GASMEMBER_GAS' : _("A money transfer related to a gas member"),
     'RECYCLE' : _("Refund for an empty container returned"),
     'ADJUST' : _("An arbitrary money transfer"),
     'GAS_EXTRA' : _("An extra money transfer related to a GAS"),
}

TRANSACTION_TYPES = TRANSACTION_TYPES_D.items()
