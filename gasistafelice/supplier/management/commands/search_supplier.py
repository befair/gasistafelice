
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from gasistafelice.supplier.models import Supplier
from gasistafelice.lib.djangolib import get_qs_filter_dict_from_str, get_instance_dict_from_attrs
from gasistafelice.lib import get_params_from_template


class Command(BaseCommand):
    args = "<python string template> [querySet filter]"
    help = 'Search for supplier using querySet filter and diplay them in python templates'

    def handle(self, *args, **options):
        
        try:
            tmpl = args[0]
        except:
            raise CommandError("Usage search_supplier: %s" % (self.args))

        if len(args) == 2:

            try:
                flt = get_qs_filter_dict_from_str(args[1])
            except ValueError:
                raise CommandError("Wrong QuerySet filter specified. It has to be in form par1=val1 OR par1=val1,par2,val2...")
            qs = Supplier.objects.filter(**flt)
        else:
            qs = Supplier.objects.all()
            
        
        attr_names = get_params_from_template(tmpl)

        for p in qs:
            d = get_instance_dict_from_attrs(p, attr_names)
            print(tmpl % d)
            
        return 0
