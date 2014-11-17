#----- Gasiste Felice page building (by fero) ------#

from django.db import models
from django.utils.translation import ugettext_lazy as _, string_concat, ugettext
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from flexi_auth.models import ParamRole
from consts import GAS_MEMBER
from des.models import Siteattr
from app_gas.models import GASMember
from django.core.urlresolvers import reverse

class Page(models.Model):
    """Page appeareance change basing on a combination of role, user and resource type.

    If you need you can specify a page structure even for a specific resource.
    The basic needing is to respect user roles, i.e.:

    * supplier should see how to manage his stock
    * gas member should see how to order
    * ...
    """

    role = models.ForeignKey(ParamRole)
    user = models.ForeignKey(User, null=True, blank=True)

    resource_ctype = models.ForeignKey(ContentType)
    resource_id = models.PositiveIntegerField(null=True, blank=True)
    # AAA: be careful that resource_id can be null!
    resource = generic.GenericForeignKey(ct_field="resource_ctype", fk_field="resource_id")

    # Configuration is the serialization of default_settings.RESOURCE_PAGE_BLOCKS[resource type] 
    # (or even resource in our case)
    confdata = models.TextField(default='', null=True, db_index=False, verbose_name=_('Configuration data'))

    class Meta:
        app_label = "rest"

    @classmethod
    def get_page(self, user, role, resource_type=None, resource_id=None):
        
        try:
           instance = Page.objects.get(user=user, role=role)
        except Page.DoesNotExist:
           instance = Page.objects.get(role=role)
        return instance

class HomePage(models.Model):
    """Return home page for a user with a role.

    This model is used to get the starting page of a user considering that he could
    have more than one role

    It works like this: a user with a specific role can point to a specific resource.
    If no record with the couple (user, role) is found in this model, then default algorithm
    is applied in order to retrieve the default bound resource.

    """

    role = models.ForeignKey(ParamRole)
    user = models.ForeignKey(User)

    # Custom home page binding
    resource_ctype = models.ForeignKey(ContentType)
    resource_id = models.PositiveIntegerField()
    resource = generic.GenericForeignKey(ct_field="resource_ctype", fk_field="resource_id")

    class Meta:
        app_label = "rest"

    @classmethod
    def get_user_home(cls, user, role):

        try:
            instance = HomePage.objects.get(user=user, role=role)
            resource = instance.resource
           
        except HomePage.DoesNotExist:

            # Default algorithm to identify default resource for a user

            if role.role.name == GAS_MEMBER:
                resource = GASMember.objects.get(gas=role.gas, person__user=user)
            else:
                resource = role.params[0].value

        return get_absolute_page_url_for_resource(resource)

def get_absolute_page_url_for_resource(resource):

    rest_part = reverse("rest.views.resource_page", kwargs={
        'resource_type': resource.resource_type,
        'resource_id': resource.pk
    })

    base_url = reverse("base.views.index")
    rest_ui_url = reverse("rest.views.index", args=[], kwargs={})
    return "%s#%s" % (rest_ui_url, rest_part[len(base_url):])

