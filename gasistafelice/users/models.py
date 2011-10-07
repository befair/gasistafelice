from django.db import models

from django.utils.translation import ugettext_lazy as _, string_concat, ugettext
from django.contrib.auth.models import User, Group

from flexi_auth.models import ParamRole, PrincipalParamRoleRelation

class UserProfile(models.Model):

    user = models.OneToOneField(User, unique=True)
    default_role = models.ForeignKey(ParamRole)

    def __unicode__(self):
        return _("Profile for %(user)s") % { 'user' : self.user }

#-----------------------------------------------------------------------------#
# SIGNALS                                                                     #
#-----------------------------------------------------------------------------#

from django.db.models.signals import post_save

def set_default_role(u, ppr):
    try:
        profile = u.get_profile()
        default_role = profile.default_role
    except UserProfile.DoesNotExist:
        up = UserProfile(user=u, default_role=ppr.role)
        up.save()


def on_principal_param_role_save(sender, **kwargs):
    ppr = kwargs['instance']
    created = kwargs['created']

    p = ppr.principal #Principal can be a User or a Group

    if created:
        # Set default role for user if it is not set

        if isinstance(p, Group):

            for u in p.user_set.all():
                set_default_role(u, ppr)

        else:
            set_default_role(p, ppr)

post_save.connect(on_principal_param_role_save, sender=PrincipalParamRoleRelation)
