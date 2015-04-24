
import notification

from gasistafelice.des_notification.models import FakeRecipient

import datetime

#-------------------------------------------------------------------------------

from django.conf import settings

def send_revisions(gas, unique=True):
    """
    Send SupplierStock object revisions to gas activists
    """
    #TODO verity date
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=gas.config.digest_days_interval)

    if unique:
        versions = gas.stocks_versions(start_date,end_date)
    else:
        versions = gas.stocks_versions_with_duplicates(start_date,end_date)
        
    if not settings.DEBUG:
        recipients = [FakeRecipient(gas.orders_email_contact)]
    else:
        #recipients = list(set(gas.tech_referrers) | set(gas.cash_referrers) | set(gas.supplier_referrers)) 
        recipients = set(gas.tech_referrers | gas.cash_referrers | gas.supplier_referrers) 
   
    notification.models.send(recipients, "catalogs_digest", {
        'start_date' : start_date,
        'end_date' : end_date,
        'gas' : gas,
        'versions' : versions,
    }, on_site=False)

#-------------------------------------------------------------------------------

def send_revisions_with_duplicates(gas):
    """GAS notification for closing orders."""

    send_revisions(gas,unique=False)
