
from django.contrib.auth.models import User
import notification

from gasistafelice.gas.models import GASSupplierSolidalPact, GASMember
from gasistafelice.des_notification.models import FakeRecipient

import datetime

#-------------------------------------------------------------------------------

def send_gas_notification(gas):
    """GAS notification for closing orders."""

    t = datetime.timedelta(gas.config.notice_days_before_order_close)
    end_date = datetime.datetime.now() + t
    start_date = end_date - datetime.timedelta(1)

    closing_orders = gas.orders.filter(datetime_end__range=(start_date, end_date))

    if not settings.DEBUG:
        recipients = [FakeRecipient(gas.orders_email_contact)]
    else:
        recipients = User.objects.filter(is_superuser=True)
    
    notification.send(recipients, "gas_notification", {
        'gas' : gas,
        'closing_orders' : closing_orders,
    }, on_site=False)
        
#-------------------------------------------------------------------------------

def send_gas_newsletter(gas):

    week = datetime.timedelta(7)

    # What will be
    end_date = start_date + week
    start_date = datetime.datetime.now()
    closing_orders = gas.orders.filter(datetime_end__range=(start_date, end_date))

    # What has been
    start_date = datetime.datetime.now() - week
    end_date = datetime.datetime.now()
    open_orders = gas.orders.open().filter(datetime_start__range=(start_date, end_date))
    new_pacts = GASSupplierSolidalPact.history.filter(history_type="+", history_date__range=(start_date, end_date))
    new_gasmembers = GASMember.history.filter(history_type="+", history_date__range=(start_date, end_date))
    old_gasmembers = GASMember.history.filter(history_type="-", history_date__range=(start_date, end_date))

    if not settings.DEBUG:
        recipients = [FakeRecipient(gas.orders_email_contact)]
    else:
        recipients = User.objects.filter(is_superuser=True)

    notification.send(recipients, "gas_newsletter", {
        'gas' : gas,
        'closing_orders' : closing_orders,
        'open_orders' : open_orders,
        'new_pacts' : new_pacts,
        'new_gasmembers' : new_gasmembers,
        'old_gasmembers' : old_pacts,
    }, on_site=False)

