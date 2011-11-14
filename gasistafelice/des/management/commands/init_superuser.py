
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from flexi_auth.models import Param, ParamRole, PrincipalParamRoleRelation

from gasistafelice.consts import DES_ADMIN
from gasistafelice.des.models import DES, Siteattr
from gasistafelice.base.models import Person
from gasistafelice.des import models

from django.conf import settings

import time

class Command(BaseCommand):
    args = ""
    help = 'Initialize DES attributes and the super user'

    def handle(self, *args, **options):
        
        # Initialize DES
        Siteattr.set_attribute("name", settings.INIT_OPTIONS['sitename'], "site name")
        Siteattr.set_attribute("descr", settings.INIT_OPTIONS['sitedescription'], "site description")
        
        des = DES.objects.all()[0]
        des.domain=settings.INIT_OPTIONS['domain'] 
        des.name=settings.INIT_OPTIONS['sitename']
        des.cfg_time=time.time()
        des.save()

        # Initialize Superuser
        su, created = User.objects.get_or_create(username=settings.INIT_OPTIONS['su_username'],
            is_superuser=True, is_staff=True)

        if created:
            su.first_name=settings.INIT_OPTIONS['su_name']
            su.last_name=settings.INIT_OPTIONS['su_surname']
            su.email=settings.INIT_OPTIONS['su_email']
            su.set_password(settings.INIT_OPTIONS['su_passwd'])
            su.save()

        p, created = Person.objects.get_or_create(user=su)
        if created:
            p.display_name="%s %s" % (su.first_name, su.last_name)
            p.name=su.first_name
            p.surname=su.last_name
            p.save()

        # Add super user to DES_ADMIN role
        pr = ParamRole.get_role(DES_ADMIN, des=des)
        PrincipalParamRoleRelation.objects.get_or_create(user=su, role=pr)

