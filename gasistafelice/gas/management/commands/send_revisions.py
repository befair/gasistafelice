
from django.core.management.base import BaseCommand, CommandError

from gasistafelice.des_notification.base  import send_revisions 
from gasistafelice.gas.models.base import GAS


class Command(BaseCommand):
    args = "<gas_pk>"
    help = 'Send an email with SupplierStock revisions for a particular GAS'

    def handle(self, *args, **options):
        """usage sample: $ python manage.py send_revisions <gas_pk>"""
        try:
            gas_pk = int(args[0])
        except:
            raise CommandError("Usage send_revisions: %s" % (self.args))

        try:
            send_revisions(GAS.objects.get(pk=gas_pk))

        except Exception as e:
            raise CommandError("send_revisions error=%s" % e)

        return 0

