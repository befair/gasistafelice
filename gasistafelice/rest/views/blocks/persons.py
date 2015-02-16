from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from flexi_auth.models import ObjectWithContext
from ajax_select.fields import autoselect_fields_check_can_add

from rest.views.blocks.base import BlockWithList, ResourceBlockAction
from consts import CREATE
from app_base.models import Person
from app_base.forms import AddPersonForm
from des.models import Siteattr

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "persons"
    BLOCK_DESCRIPTION = _("People")
    BLOCK_VALID_RESOURCE_TYPES = ["site"] 

    def _get_resource_list(self, request):
        return request.resource.persons.order_by('?')[:50]

    def _get_user_actions(self, request):

        user_actions = []
        ctx = { 'site' : Siteattr.get_site() }
        if request.user.has_perm(CREATE, obj=ObjectWithContext(Person, context=ctx)):

            user_actions.append( 
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE, verbose_name=_("Add person"),
                    #WAS admin: url=urlresolvers.reverse('admin:base_person_add')
                )
            )

        return user_actions
        
    def _get_add_form_class(self):
        form_class = AddPersonForm
        autoselect_fields_check_can_add(form_class, Person, self.request.user)
        return form_class

