from django.db.models.signals import post_syncdb
from django.contrib.auth.models import User

from flexi_auth.models import Param, ParamRole, PrincipalParamRoleRelation

from gasistafelice.consts import DES_ADMIN
from gasistafelice.des.models import DES, Siteattr
from gasistafelice.base.models import Person

from django.conf import settings

def init_superuser(sender, app, created_models, verbosity, **kwargs): 

    if DES in created_models:

        # Initialize DES
        des, created = DES.objects.get_or_create(
            domain=settings.INIT_OPTIONS['domain'], 
            name=settings.INIT_OPTIONS['sitename'],
        )
        if created:
            des.cfg_time=1
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

post_syncdb.connect(init_superuser)
