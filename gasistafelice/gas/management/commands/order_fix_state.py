
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from gasistafelice.gas.models import GASSupplierOrder


class Command(BaseCommand):
    args = ""
    help = """Fix order states according to their datetime and state settings.

* Open orders that are in "prepared" state and datetime_start <= datetime.now()
* Close orders that are in "open" state and datetime_end >= datetime.now()
"""

    def handle(self, *args, **options):

        for order in GASSupplierOrder.objects.prepared():
            order.open_if_needed()

        for order in GASSupplierOrder.objects.open():
            order.close_if_needed()
            
        return 0
