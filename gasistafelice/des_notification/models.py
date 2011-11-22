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
    msg = _("Product %(product)s: has been erased from order %(order)s") % {
            'product' : gmo.product,
            'order' : gmo.order,
    }

    gmo.gasmember.person.user.message_set.create(message=msg)

#-------------------------------------------------------------------------------

def notify_gmo_price_update(sender, **kwargs):

    gmo = sender
    old_price = gmo.ordered_price
    new_price = gmo.ordered_product.order_price
    msg = _("Product %(product)s: updated price from %(old_price)s to %(new_price)s") % {
            'product' : gmo.product,
            'old_price' : old_price,
            'new_price' : new_price,
    }

    gmo.gasmember.person.user.message_set.create(message=msg)

#-------------------------------------------------------------------------------

def notify_gasstock_product_enabled(sender, **kwargs):

    gasstock = sender
    msg = _("Product %(product)s is now available for %(gas)s") % {
            'product' : gasstock.product,
            'gas' : gasstock.gas
    }

    for gm in gasstock.gasmembers:
        #TODO: check for user settings and see if user wants to be notified
        # via messages, mail or both
        gm.person.user.message_set.create(message=msg)

#-------------------------------------------------------------------------------

def notify_gasstock_product_disabled(sender, **kwargs):

    gasstock = sender
    msg = _("Product %(product)s has been disabled for %(gas)s") % {
            'product' : gasstock.product,
            'gas' : gasstock.gas
    }

    for gm in gasstock.gasmembers:
        #TODO: check for user settings and see if user wants to be notified
        # via messages, mail or both
        gm.person.user.message_set.create(message=msg)

#-------------------------------------------------------------------------------

def notify_order_open(sender, **kwargs):

    order = sender
    msg = _('Order related to %(pact)s has been created. Check it at <a href="%(url)s">%(url)s</a>') % {
            'pact' : order.pact,
            'url' : order.get_absolute_url()
    }

    for gm in order.gasmembers:
        #TODO: check for user settings and see if user wants to be notified
        # via messages, mail or both
        gm.person.user.message_set.create(message=msg)

#-------------------------------------------------------------------------------

def notify_order_state_update(sender, **kwargs):

    order = sender
    transition = kwargs['transition']

    extra_content = {
        'gas' : order.gas,
        'order' : order,
    }

    if transition.destination == "closed":
        msg = _('Order related to %(pact)s has been closed. Check it at <a href="%(url)s">%(url)s</a>') % {
                'pact' : order.pact,
                'url' : order.get_absolute_url()
        }

        notification.send(order.referrers, "order_closed", 
            extra_content, on_site=True
        )
        #WAS: refs.message_set.create(message=msg)

    elif transition.destination == "finalized":

        notification.send(order.referrers | order.supplier.referrers, 
            "order_sent", extra_content, on_site=True
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
        "order_sent", _("Order Sent by a GAS"), 
        _("an order has been sent by a GAS to involved supplier"), default=2
    )
    
    notification.create_notice_type(
        "order_open", _("Order open"), 
        _("an order has been opened"), default=3
    )
    
    notification.create_notice_type(
        "order_closed", _("Order closed"), 
        _("an order has been closed"), default=3
    )
    
    notification.create_notice_type(
        "gmo_product_erased", _("Product erased from order"), 
        _("an ordered product is not available anymore"), default=3
    )
    
    notification.create_notice_type(
        "gmo_price_update", _("Product changed price"), 
        _("an ordered product has changed price"), default=3
    )
    
    notification.create_notice_type(
        "order_state_update", _("Order state update"), 
        _("an order has been updated"), default=3
    )
    
    notification.create_notice_type(
        "gasstock_product_enabled", _("Product enabled for GAS"), 
        _("a product has been enabled for GAS"), default=3
    )
    
    notification.create_notice_type(
        "gasstock_product_disabled", _("Product disabled for GAS"), 
        _("a product has been disabled for GAS"), default=3
    )
    
models.signals.post_syncdb.connect(create_notice_types, sender=notification)
