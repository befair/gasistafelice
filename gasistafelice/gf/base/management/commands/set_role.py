
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from flexi_auth.models import ParamRole, PrincipalParamRoleRelation, Param

from middleware import get_resource_by_path

import logging

log = logging.getLogger(__name__)


class Command(BaseCommand):
    args = "<username> <role_name> <resource_type> <resource_id>"
    help = 'Set a role for a user'

    def handle(self, *args, **options):
        
        try:
            username = args[0]
            role_name = args[1]
            resource_type = args[2]
            resource_id = args[3]
        except:
            raise CommandError("Usage set_role: %s" % (self.args))

        log.info("Setting role for %s" % username)


        u = User.objects.get(username=username)
        resource = get_resource_by_path(resource_type, resource_id)
        ctype = ContentType.objects.get_for_model(resource.__class__)
        params = Param.objects.filter(content_type=ctype, object_id=resource.pk)

        pr = ParamRole.objects.get(role__name=role_name, param_set=params)
        x, created = PrincipalParamRoleRelation.objects.get_or_create(role=pr, user=u)
        if not created:
            log.info("Role %s for user %s already exists" % (pr, u))

        return 0
