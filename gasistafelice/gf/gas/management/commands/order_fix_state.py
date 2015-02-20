
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from gf.gas.models import GASSupplierOrder


class Command(BaseCommand):
    args = ""
    help = """Fix order states according to their datetime and state settings.

* Open orders that are in "prepared" state and datetime_start <= datetime.now()
* Close orders that are in "open" state and datetime_end >= datetime.now()
"""

    def handle(self, *args, **options):

        for order in GASSupplierOrder.objects.prepared():
            #Pass argument for issuer is cron job. The function will send email if necesary
            order.open_if_needed(True)

        for order in GASSupplierOrder.objects.open():
            #Pass argument for issuer is cron job. The function will send email if necesary
            order.close_if_needed()
            
        return 0
