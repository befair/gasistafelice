from django.db.models.signals import post_syncdb
from django.contrib.admin.models import User

from gasistafelice.des.management.commands import init_superuser
from gasistafelice.des import models as des_models

def init_superuser(sender, app, created_models, verbosity, **kwargs): 

    if User in created_models:

        cmd = init_superuser.Command()
        cmd.handle()

post_syncdb.connect(init_superuser, sender=des_models)

