
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from gf.base.management.commands import set_role
import consts

class Command(BaseCommand):
    args = "<gas_pk> <username>"
    help = 'Set GAS_REFERRER_TECH to username for GAS identified by gas pk'

    def handle(self, *args, **options):
        
        try:
            gas_pk = args[0]
            username = args[1]
        except:
            raise CommandError("Usage set_gas_referrer_tech: %s" % (self.args))

        resource_type = "gas"
        resource_id = gas_pk
        role_name = consts.GAS_REFERRER_TECH
        
        cmd = set_role.Command()
        return cmd.handle(username, role_name, resource_type, resource_id)

