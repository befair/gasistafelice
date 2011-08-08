#----- Gasiste Felice page building (by fero) ------#

from django.db import models
from django.utils.translation import ugettext_lazy as _, string_concat, ugettext
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from gasistafelice.auth.models import Role
from gasistafelice.des.models import Siteattr
from django.core.urlresolvers import reverse

class Page(models.Model):
    """Page appeareance change basing on a combination of role, user and resource type.

    If you need you can specify a page structure even for a specific resource.
    The basic needing is to respect user roles, i.e.:

    * supplier should see how to manage his stock
    * gas member should see how to order
    * ...
    """

    role = models.ForeignKey(Role)
    user = models.ForeignKey(User, null=True)

    resource_ctype = models.ForeignKey(ContentType)
    resource_id = models.PositiveIntegerField(null=True)
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
    """

    role = models.ForeignKey(Role)
    user = models.ForeignKey(User, null=True)

    class Meta:
        app_label = "rest"

    # Home page bindings
    resource_ctype = models.ForeignKey(ContentType)
    resource_id = models.PositiveIntegerField()
    resource = generic.GenericForeignKey(ct_field="resource_ctype", fk_field="resource_id")

    def get_absolute_url(self):
        rest_part = reverse("rest.views.resource_page", kwargs={
            'resource_type': self.resource.resource_type,
            'resource_id': self.resource.resource_id
        })

        base_url = reverse("base.views.index")
        rest_ui_url = reverse("rest.views.index", args=[], kwargs={})

        return "%s#%s" % (rest_ui_url, rest_part[len(base_url):])


    @classmethod
    def get_user_url(cls, user, role):
        try:
           instance = HomePage.objects.get(user=user, role=role)
        except HomePage.DoesNotExist:
            try:
                instance = HomePage.objects.get(role=role)
            except HomePage.DoesNotExist:
                instance = None

        if instance:
            rv = instance.get_absolute_url()
        else:
            rv = reverse("rest.views.index")

        return rv


