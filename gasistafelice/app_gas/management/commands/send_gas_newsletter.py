
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from app_gas.models import GAS, GASMember
from app_supplier.models import Supplier, Product #, HistoricalSupplier

from datetime import tzinfo, timedelta, datetime

class Command(BaseCommand):
    args = ""
    help = 'For each GAS in the des, send weekly newsletter info'

    def handle(self, *args, **options):
        """usage sample: $ python manage.py send_gas_newsletter """
        g = 0
        gm = 0
        s = 0
        p = 0
        des_msg = ''
        gas_msg = ''
        _msg = None
        Monday_day = first_day_on_or_after(0, datetime.now())
        Sunday_day = first_day_on_or_after(6, datetime.now())
        try:

            #TODO New Supplier
            for supplier in Supplier.objects.filter(
            #for hist_supplier in HistoricalSupplier.objects.filter(
            #for hist_supplier in Supplier.objects.filter(history_date__range):
            #for hist_supplier in HistoricalSupplier.objects.filter(
                history_date__gte=Monday_day,
                history_date__lte=Sunday_day ):
                #supplier = Supplier.objects.get(hist_supplier.id)
                s = supplier.pk
                print supplier
                _msg.append('E stato registrato uno nuovo fornitore %s' % (gasmember))

#            #TODO New Product
#            for product in Product.objects.filter():
#                p = product.pk
#                print product

#            #TODO New Category
#            for product in Product.objects.filter():
#                g = gas.pk
#                print gas

            for gas in GAS.objects.all():
                g = gas.pk
                print gas
                #TODO: Welcome New Gassista
                for gasmember in gas.gasmembers:
                    gm = gasmember.pk
                    print gasmember
                    _msg.append('Something to say %s' % (gasmember))

                #TODO Changed Price Product

                #TODO Welcome New PACT

                #TODO: Economic Info
                #fee
                #Alert negative State under Threshold (only for private GASMember email)...

                if len(_msg) > 0:
                    _destinary = gas
                    print '---------------SEND EMAIL FOR ONE GAS (%s) and continue if other GAS todo-----' % (_destinary)


            #tmpl = args[0]
        except:
            raise CommandError("send_gas_newsletter (%s/%s) last_msg: %s" % (g,gm,_msg))

        #print((tmpl % d).encode('UTF-8'))
        return 0

def first_day_on_or_after(daynum, dt):
    days_to_go = daynum - dt.weekday()
    if days_to_go:
        dt += timedelta(days_to_go)
    return dt
