
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import get_model
from django.db.models.query import QuerySet

from gasistafelice.lib.djangolib import get_qs_filter_dict_from_str, get_instance_dict_from_attrs
from gasistafelice.lib import get_params_from_template

import logging

log = logging.getLogger(__name__)


class Command(BaseCommand):
    args = "<app.model> <python_template> [querySet filter]"
    help = 'Print a querySet following a template'

    def handle(self, *args, **options):
        
        try:
            model_name = args[0]
            tmpl = args[1]
        except:
            raise CommandError("Usage print_qs: %s" % (self.args))

        try:
            model = get_model(*model_name.split('.'))
        except:
            raise CommandError("No model %s found in app %s" % model_name.split('.'))

        if len(args) == 3:

            try:
                flt = get_qs_filter_dict_from_str(args[2])
            except ValueError:
                raise CommandError("Wrong QuerySet filter specified. It has to be in form par1=val1 OR par1=val1,par2,val2...")
            qs = model.objects.filter(**flt)
        else:
            qs = model.objects.all()
            
        attr_names = get_params_from_template(tmpl)

        for p in qs:
            d = get_instance_dict_from_attrs(p, attr_names)
            for k,v in d.items():
                if isinstance(v, QuerySet):
                    qs = []
                    for el in v:
                        qs.append(el.__unicode__())
                    d[k] = qs
            print(tmpl % d).encode('utf-8')
            
        return 0
            
