
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from gasistafelice.gas.models import GAS, GASMember
from gasistafelice.lib.djangolib import get_qs_filter_dict_from_str, get_instance_dict_from_attrs
from gasistafelice.lib import get_params_from_template


class Command(BaseCommand):
    args = "<python string template> [querySet filter]"
    help = 'Search for gasmember using querySet filter and diplay them in python templates'

    def handle(self, *args, **options):
        """usage sample: $ python manage.py search_gasmember '%(statistic_name)s' """
        try:
            tmpl = args[0]
        except:
            raise CommandError("Usage search_gasmember: %s" % (self.args))

        if len(args) == 2:

            try:
                flt = get_qs_filter_dict_from_str(args[1])
            except ValueError:
                raise CommandError("Wrong QuerySet filter specified. It has to be in form par1=val1 OR par1=val1,par2,val2...")
            qs = GASMember.objects.filter(**flt)
        else:
            qs = GASMember.objects.all()
            
        
        attr_names = get_params_from_template(tmpl)

        #for p in qs.order_by('gas__id_in_des','person__surname'):
        for p in qs.order_by('person__surname'):
            d = get_instance_dict_from_attrs(p, attr_names)
            print((tmpl % d).encode('UTF-8'))
            
        return 0

