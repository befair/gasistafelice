from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from flexi_auth.models import ObjectWithContext

from gasistafelice.rest.views.blocks.base import BlockWithList, ResourceBlockAction
from gasistafelice.consts import CREATE
from gasistafelice.base.models import Person
from gasistafelice.base.forms import AddPersonForm
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
       #was:  if request.user.has_perm(CREATE, obj=ObjectWithContext(Person, context=ctx)):
        if request.user.has_perm(CREATE, obj=ObjectWithContext(request.resource
)):
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
        return AddPersonForm
        #WAS: raise NotImplementedError("The add form page in use now is the admin interface page.")

