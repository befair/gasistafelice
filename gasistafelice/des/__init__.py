from django.db.models.signals import post_syncdb

from des.management.commands import init_superuser
from des import models as des_models

## Cannot execute init_superuser because we need fixtures applied!
#def init_su(sender, app, created_models, verbosity, **kwargs): 
#
#    if des_models.DES in created_models:
#
#        cmd = init_superuser.Command()
#        cmd.handle()
#
#post_syncdb.connect(init_su, sender=des_models)
#
