"""View for block details specialized for GASMember in Person page"""

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from rest.views.blocks import gasmembers


class Block(gasmembers.Block):

    BLOCK_NAME = "person_gasmembers"
    BLOCK_VALID_RESOURCE_TYPES = ["person"] 

    def _get_user_actions(self, request):

        return []

    def get_description(self):
        return _("%(name)s's GAS memberships") % {
            'name' : self.resource.person.name,
        }

