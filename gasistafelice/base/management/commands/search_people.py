
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from gasistafelice.base.models import Person
import re


class Command(BaseCommand):
    args = "<python string template> [querySet filter]"
    help = 'Search for people using querySet filter and diplay them in python templates'

    def handle(self, *args, **options):

        
        try:
            tmpl = args[0]
        except:
            raise CommandError("Usage search_person: %s" % (self.args))

        if len(args) == 2:

            flt = {}
            flt_string = args[1]

            # build filter
            if "," not in flt_string: 
                try:
                    k,v = flt_string.split('=')
                except ValueError:
                    raise CommandError("Wrong QuerySet filter specified. It has to be in form par1=val1 OR par1=val1,par2,val2...")
                flt[k] = v

            else:
                for couple in flt_string.split(','):
                    try:
                        k,v = couple.split('=')
                    except ValueError:
                        raise CommandError("Wrong QuerySet filter specified. It has to be in form par1=val1 OR par1=val1,par2,val2...")
                    flt[k] = v

            qs = Person.objects.filter(**flt)

        else:
            
            qs = Person.objects.all()
            
        
        # split python template
        expr = r"%\((.*?)\)"
        r = re.compile(expr)
        # find attributes
        attr_names = r.findall(tmpl)

        for p in qs:
            d = {}
            
            for attr_name in attr_names:
                # retrieve attributes and build dict for template
                attr = getattr(p, attr_name)
                if callable(attr):
                    v = attr()
                else:
                    v = attr
                d[attr_name] = v
            
            print(tmpl % d)
            
        return 0
