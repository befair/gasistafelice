
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import get_model


from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from gasistafelice.middleware import get_resource_by_path
from flexi_auth.models import ParamRole, PrincipalParamRoleRelation, Param
import os, logging, datetime

from django.db import transaction

log = logging.getLogger(__name__)
if settings.LOG_FILE:

    if not log.handlers:
        log.setLevel( logging.INFO )
        hdlr = logging.FileHandler(settings.LOG_FILE)
        hdlr.setFormatter( logging.Formatter('%(asctime)s %(levelname)s %(message)s') )
        log.addHandler(hdlr)


class Command(BaseCommand):
    args = "<app.model> <python_template>"
    help = 'Print a querySet following a template'

    def handle(self, *args, **options):
        
        try:
            model_name = args[0]
            python_template = args[1]
        except:
            raise CommandError("Usage print_qs: %s" % (self.args))

        try:
            model = get_model(*model_name.split('.'))
        except:
            raise CommandError("No model %s found in app %s" % model_name.split('.'))
            

        for el in model.objects.all():
            rv = python_template % el.__dict__
            print rv.encode('UTF-8')

        return 0
