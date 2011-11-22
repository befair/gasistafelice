"""Receive signals and notify users"""

from django.db import models
from django.utils.translation import ugettext as _

from notification import models as notification
        
from gasistafelice.gas.models import GAS
from gasistafelice.gas import signals as gas_signals

#-------------------------------------------------------------------------------

class FakeRecipient(object):

    def __init__(self, email):
        self.email = email

#-------------------------------------------------------------------------------


def notify_gmo_product_erased(sender, **kwargs):

    gmo = sender
    extra_content = {
        'order' : gmo.order,
        'product' : gmo.product,
        'action' : _("erased"),
    }

    recipients = [gmo.gasmember.person.user]

    notification.send(recipients, "ordered_product_update", 
        extra_content, on_site=True
    )

#-------------------------------------------------------------------------------

def notify_gmo_price_update(sender, **kwargs):

    gmo = sender
    old_price = gmo.ordered_price
    new_price = gmo.ordered_product.order_price
    extra_content = {
        'order' : gmo.order,
        'product' : gmo.product,
        'action' : _("price changed"),
        'extra_append' : _("from %(old)s to %(new)s") % (old_price, new_price),
    }

    recipients = [gmo.gasmember.person.user]

    notification.send(recipients, "ordered_product_update", 
        extra_content, on_site=True
    )

#-------------------------------------------------------------------------------

def notify_gasstock_product_enabled(sender, **kwargs):

    gasstock = sender
    extra_content = {
        'gas' : gasstock.gas,
        'product' : gasstock.product,
        'action' : _("enabled"),
    }

    recipients = User.objects.filter(
        person.gasmember_set__in=gasstock.gasmembers
    ).distinct()

    notification.send(recipients, "gasstock_update", 
        extra_content, on_site=True
    )

#-------------------------------------------------------------------------------

def notify_gasstock_product_disabled(sender, **kwargs):

    gasstock = sender
    extra_content = {
        'gas' : gasstock.gas,
        'product' : gasstock.product,
        'action' : _("disabled"),
    }

    recipients = User.objects.filter(
        person.gasmember_set__in=gasstock.gasmembers
    ).distinct()

    notification.send(recipients, "gasstock_update", 
        extra_content, on_site=True
    )


#-------------------------------------------------------------------------------

def notify_order_state_update(sender, **kwargs):

    order = sender
    transition = kwargs['transition']

    extra_content = {
        'gas' : order.gas,
        'order' : order,
        'action' : transition.name,
        'state' : transition.destination,
    }

    if transition.destination in ["open", "closed"]:
        recipients = order.referrers
    else:
        recipients = order.referrers | order.supplier.referrers

    notification.send(recipients, "order_state_update", 
        extra_content, on_site=True
    )

#-------------------------------------------------------------------------------


gas_signals.order_open.connect(notify_order_open)
gas_signals.order_state_update.connect(notify_order_state_update)
gas_signals.gmo_price_update.connect(notify_gmo_price_update)
gas_signals.gmo_product_erased.connect(notify_gmo_product_erased)
gas_signals.gasstock_product_enabled.connect(notify_gasstock_product_enabled)
gas_signals.gasstock_product_disabled.connect(notify_gasstock_product_disabled)

def create_notice_types(app, created_models, verbosity, **kwargs):
    """Define notice types and default 'spam_sensitivity'.

    `spam_sensitivity` states default for sending message through a `backend`.
    If `spam_sensitivity` if > than `backend.spam_sensitivity`, then message is
    not sent through that medium.

    `EmailBackend.spam_sensitivity` = 2

    This in turn is saved as a default `NoticeSetting` that could be (eventually)
    changed by User in notification preferences panel.
    """
    
    # Mail notifications
    notification.create_notice_type(
        "gasmember_notification", _("Notification Received"), 
        _("you have received a notification"), default=2,
    )

    notification.create_notice_type(
        "gas_notification", _("Notification Received"), 
        _("this GAS has received a notification"), default=2
    )
    
    notification.create_notice_type(
        "gas_newsletter", _("Newsletter Received"), 
        _("this GAS has received the newsletter"), default=2
    )
    
    notification.create_notice_type(
        "order_state_update", _("Order state updated"), 
        _("an order has been updated"), default=2
    )
    
    # Web notifications
    notification.create_notice_type(
        "ordered_product_update", _("Ordered product update"), 
        _("an ordered product has changed"), default=3
    )
    
    notification.create_notice_type(
        "gasstock_update", _("Product update for GAS"), 
        _("a product has been updated for GAS"), default=3
    )
    
models.signals.post_syncdb.connect(create_notice_types, sender=notification)
