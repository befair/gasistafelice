"""Receive signals and notify users"""

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from notification import models as notification
        
from gasistafelice.gas.models import GAS
from gasistafelice.gas import signals as gas_signals
from gasistafelice.lib import unordered_uniq

from gasistafelice.des.models import Siteattr

import logging

log = logging.getLogger(__name__)

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

    try:
        notification.send(recipients, "ordered_product_update", 
            extra_content
        )
    except Exception as e:
        log.error("Send msg notify_gmo_product_erased: %s (%s)" % (e.message, type(e)))
        log.error('EEEEEEEEEEEEEE  notification notify_gmo_product_erased %s (%s)' % (e.message, type(e)))
        pass

#-------------------------------------------------------------------------------

def notify_gmo_price_update(sender, **kwargs):

    gmo = sender
    old_price = gmo.ordered_price
    new_price = gmo.ordered_product.order_price
    extra_content = {
        'order' : gmo.order,
        'product' : gmo.product,
        'action' : _("price changed"),
        'extra_append' : _("from %(old)s to %(new)s") % ({ 'old' : old_price, 
            'new' : new_price
        }),
    }

    recipients = [gmo.gasmember.person.user]

    try:
        notification.send(recipients, "ordered_product_update", 
            extra_content
        )
    except Exception as e:
        log.error("Send msg notify_gmo_price_update: %s (%s)" % (e.message, type(e)))
        log.error('EEEEEEEEEEEEEE  notification notify_gmo_price_update %s (%s)' % (e.message, type(e)))
        pass

#-------------------------------------------------------------------------------

def notify_gasstock_product_enabled(sender, **kwargs):

    gasstock = sender
    extra_content = {
        'gas' : gasstock.gas,
        'product' : gasstock.product,
        'action' : _("enabled"),
    }

#Cannot resolve keyword 'gasmember_set' into field. Choices are: address, avatar, contact_set, delivery_for_order_set, des, display_name, gas, gasactivist, gasmember, historicaldelivery_for_order_set, historicalgasactivist, historicalgasmember, historicalorder_set, historicalsupplier_frontman_set, historicalsupplieragent, historicalwithdrawal_for_order_set, id, name, order_set, ssn, supplier, supplier_frontman_set, supplieragent, surname, user, website, withdrawal_for_order_set
    recipients = User.objects.filter(
#        person__gasmember_set__in=gasstock.gasmembers
        person__gasmember__in=gasstock.gasmembers
    ).distinct()

    log.debug("notify_gasstock_product_enabled recipients %s " % recipients)

    try:
        notification.send(recipients, "gasstock_update", 
            extra_content
        )
    except Exception as e:
        log.error("Send msg notify_gasstock_product_enabled: %s (%s)" % (e.message, type(e)))
        log.debug('EEEEEEEEEEEEEE  notification notify_gasstock_product_enabled %s (%s)' % (e.message, type(e)))
        pass

#-------------------------------------------------------------------------------

def notify_gasstock_product_disabled(sender, **kwargs):

    gasstock = sender
    extra_content = {
        'gas' : gasstock.gas,
        'product' : gasstock.product,
        'action' : _("disabled"),
    }

    recipients = User.objects.filter(
        person__gasmember__in=gasstock.gasmembers
    ).distinct()
#        person__gasmember_set__in=gasstock.gasmembers

    try:
        notification.send(recipients, "gasstock_update", 
            extra_content
        )
    except Exception as e:
        log.error("Send msg notify_gasstock_product_disabled: %s (%s)" % (e.message, type(e)))
        log.debug('EEEEEEEEEEEEEE  notification notify_gasstock_product_disabled %s (%s)' % (e.message, type(e)))
        pass

#-------------------------------------------------------------------------------
from gasistafelice import gf_exceptions as exceptions

def notify_order_state_update(sender, **kwargs):

    order = sender
    transition = kwargs['transition']

    extra_content = {
        'gas' : order.gas,
        'order' : order,
        'action' : transition.name,
        'state' : transition.destination.name,
        'site' : Siteattr.get_site(),
        'protocol' : 'http',
    }

    #--- Transition name ---#

    recipients = []

    try:
        if transition.destination.name.lower() in ["open", "closed"]:
            recipients = [order.referrer_person.user]
        elif transition.destination.name.lower() in ["sent", "paid"]:
            recipients = list(order.supplier.referrers) + [order.referrer_person.user]
            recipients = unordered_uniq(recipients)
    except AttributeError as e:
        #TODO Matteo: complete exception handling here
        raise exceptions.ReferrerIsNoneException()

    log.debug("Transition to: %s" % transition.destination.name)
    log.debug("Recipients: %s" % zip(recipients, map(lambda x: x.email, recipients)))
    try:
        notification.send(recipients, "order_state_update", 
            extra_content
        )
    except Exception as e:
        log.error("Send msg notify_order_state_update: %s (%s)" % (e.message, type(e)))
        pass

#-------------------------------------------------------------------------------

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
    # WAS: notification.create_notice_type(
    try:
        obj, created = notification.NoticeType.objects.get_or_create(
            label="gasmember_notification", defaults = { 
                'display': _("Notification Received"), 
                'description' : _("you have received a notification"), 
                'default': 2 }
        )
    except notification.NoticeType.MultipleObjectsReturned as e:
        log.error("Found more than one notice type for label gasmember_notification")
        raise("Found more than one notice type for label gasmember_notification")
    else:
        if created:
            log.debug("Created notice type for label gasmember_notification")
        else:
            log.debug("Found existing notice type for label gasmember_notification. Not creating another one.")
            


    # WAS: notification.create_notice_type(
    try:
        obj, created = notification.NoticeType.objects.get_or_create(
            label="gas_notification", defaults = {
                'display' : _("Notification Received"), 
                'description' : _("this GAS has received a notification"),
                'default' : 2 }
        )
    except notification.NoticeType.MultipleObjectsReturned as e:
        log.error("Found more than one notice type for label gas_notification")
        raise("Found more than one notice type for label gas_notification")
    else:
        if created:
            log.debug("Created notice type for label gas_notification")
        else:
            log.debug("Found existing notice type for label gas_notification. Not creating another one")

    # WAS: notification.create_notice_type(
    try:
        obj, created = notification.NoticeType.objects.get_or_create(
            label="gas_newsletter", defaults = {
                'display' : _("Newsletter Received"), 
                'description' : _("this GAS has received the newsletter"), 
                'default' : 2 }
        )
    except notification.NoticeType.MultipleObjectsReturned as e:
        log.error("Found more than one notice type for label gas_newsletter")
        raise("Found more than one notice type for label gas_newsletter")
    else:
        if created:
            log.debug("Created notice type for label gas_newsletter")
        else:
            log.debug("Found existing notice type for label gas_newsletter. Not creating another one")

    # WAS: notification.create_notice_type(
    try:
        obj, created = notification.NoticeType.objects.get_or_create(
            label="order_state_update", defaults = { 
                'display' : _("Order state updated"), 
                'description' : _("an order has been updated"), 
                'default' : 2 }
        )
    except notification.NoticeType.MultipleObjectsReturned as e:
        log.error("Found more than one notice type for label order_state_update")
        raise("Found more than one notice type for label order_state_update")
    else:
        if created:
            log.debug("Created notice type for label order_state_update")
        else:
            log.debug("Found existing notice type for label order_state_update. Not creating another one")
    
    # Web notifications
    # WAS: notification.create_notice_type(
    try:
        obj, created = notification.NoticeType.objects.get_or_create(
            label="ordered_product_update", defaults = {
                'display' : _("Ordered product update"), 
                'description' : _("an ordered product has changed"), 
                'default' : 3 }
        )
    except notification.NoticeType.MultipleObjectsReturned as e:
        log.error("Found more than one notice type for label ordered_product_update")
        raise("Found more than one notice type for label ordered_product_update")
    else:
        if created:
            log.debug("Created notice type for label ordered_product_update")
        else:
            log.debug("Found existing notice type for label ordered_product_update. Not creating anotherw one")
    
    # WAS: notification.create_notice_type(
    try:
        obj, created = notification.NoticeType.objects.get_or_create(
            label="gasstock_update", defaults = {
                'display' : _("Product update for GAS"), 
                'description' : _("a product has been updated for GAS"), 
                'default' : 3 }
        )
    except notification.NoticeType.MultipleObjectsReturned as e:
        log.error("Found more than one notice type for label gasstock_update")
        raise("Found more than one notice type for label gasstock_update")
    else:
        if created:
            log.debug("Created notice type for label gasstock_update")
        else:
            log.debug("Found existing notice type for label gasstock_update. Not creating another one")

    
models.signals.post_syncdb.connect(create_notice_types, sender=notification)

