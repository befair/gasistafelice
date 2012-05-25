
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from gasistafelice.gas.models import GAS, GASMember

import datetime

class Command(BaseCommand):
    args = "<gas_pk>"
    help = 'Send an email with closing and delivering orders in some days specified in GAS configuration notice_days_before_order_close'

    def handle(self, *args, **options):
        """usage sample: $ python manage.py send_gas_notification"""
        try:
            gas_pk = int(args[0])
        except:
            raise CommandError("Usage send_gas_notification: %s" % (self.args))

        gas = GAS.objects.get(pk=gas_pk)

        g = 0
        o = 0
        _msg = None
        delta_day = None

        try:
            delta_day = gas.config.notice_days_before_order_close
            if delta_day:
                next_day = datetime.datetime.now()+datetime.timedelta(days=delta_day)
                # print 'next_day: %s' % next_day
                weeknumber = datetime.date.today().isocalendar()[1]
                subject = "[NEWS] %s - %s (%s)" % (gas.id_in_des, gas, weeknumber)

                if delta_day == 1:
                    pre_msg = "Domani "
                else:
                    pre_msg = "Fra %d giorni " % delta_day

                _msg = []
                g = gas.pk
                # print gas
                for order in gas.orders.open().filter(
                        datetime_end__year = next_day.year, 
                        datetime_end__month = next_day.month, 
                        datetime_end__day = next_day.day
                ):
                    o = order.pk
                    # print order
                    _msg.append("* %s si chiude l'ordine %s\n" % (pre_msg, order))
                    
                    
                # print 'next_day: %s' % next_day
                # subject = "[NEWS] %s - %s (%s)" % (gas.id_in_des, gas, weeknumber)
                if delta_day == 1:
                    pre_msg = "Domani "
                else:
                   pre_msg = "Fra %d giorni " % delta_day
                _delivery_msg = []
                # g = gas.pk
                # print gas
                for order in gas.orders.closed().filter(
                        delivery.date__year = next_day.year, 
                        delivery.date__month = next_day.month, 
                        delivery.date__day = next_day.day
                ):
                    o = order.pk
                    # print order
                    _delivery_msg.append("* %s si consegna l'ordine %s" % (pre_msg, order))
                body = u""
                if len(_msg) > 0:
                    body = "Ordini in prossima chiusura\n\n"
                    body +=  _msg.join("\n")
                    
                if len(_delivery_msg) > 0:
                    body = "\nOrdini in prossima consegna\n\n"
                    body +=  _delivery_msg.join("\n")
                    
                if body:
                    gas.send_email_to_gasmembers(subject,body)

        except Exception as e:
            raise CommandError("send_gas_notification delta_day=%s (%s/%s) last_msg: %s, error=%s" % (delta_day, g, o, _msg, e))

        return 0

