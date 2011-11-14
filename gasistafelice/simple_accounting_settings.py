from django.utils.translation import ugettext_lazy as _
TRANSACTION_TYPES = (
                     ('INVOICE_PAYMENT', _("Payment of an invoice")),
                     ('INVOICE_COLLECTION', _("Collection of an invoice")),
                     ('RECHARGE', _("Recharge made by a GAS member")),
                     ('MEMBERSHIP_FEE', _("Payment of a membership fee by a GAS member")),
                     ('PAYMENT', _("A generic payment")),
                     ('GAS_WITHDRAWAL', _("A withdrawal from a member's account made by a GAS")),
                     ('REFUND', _("A money refund made by a supplier to a GAS")),
)
