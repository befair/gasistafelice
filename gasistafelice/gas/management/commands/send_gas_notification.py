
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from gasistafelice.gas.models import GAS, GASMember

from datetime import tzinfo, timedelta, datetime

class Command(BaseCommand):
    args = "<Integer>"
    help = 'For each GAS in the des, send order information'

    def handle(self, *args, **options):
        """usage sample: $ python manage.py send_gas_notification 2"""

        try:
            delta_day = int(args[0])
        except:
            raise CommandError("Usage send_gas_notification: %s" % (self.args))

        g = 0
        o = 0
        _msg = None
        next_day = datetime.now()+timedelta(days=delta_day)
        print 'next_day: %s' % next_day
        try:
            for gas in GAS.objects.all():
                _msg = []
                g = gas.pk
                print gas
                for order in gas.orders.open().filter(
                        datetime_end__year = next_day.year, 
                        datetime_end__month = next_day.month, 
                        datetime_end__day = next_day.day):
                    o = order.pk
                    print order

                    if delta_day == 1:
                        _msg.append('Domani chiude l\'ordine per %s' % (order))
                    else:
                        _msg.append('Chiusura fra % giorni dell\'ordine %s' % (delta_day, order))
            #tmpl = args[0]

                if len(_msg) > 0:
                    print '---------------SEND EMAIL FOR ONE GAS and continue if other GAS todo-----'


        #Open order automatically without using parameter if pact.use_motor
        #Not needeed due to .open() working on date instead of workflow state


        #TODO: Close order automatically without using parameter if datetime_end is tomorow and pact.use_motor



        except:
            raise CommandError("send_gas_notification %s (%s/%s) last_msg: %s" % (delta_day, g, o, _msg))

        #print((tmpl % d).encode('UTF-8'))
        return 0

