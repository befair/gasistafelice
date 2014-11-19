"""View for block details specialized for a GASMember"""

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from rest.views.blocks import details
from gf.gas.forms.base import EditGASMemberForm

class Block(details.Block):

    BLOCK_NAME = "gasmember_details"
    BLOCK_VALID_RESOURCE_TYPES = ["gasmember"] 

    def _get_user_actions(self, request):

        return []

    def get_description(self):
        return _("%(name)s's details in %(gas)s") % {
            'name' : self.resource.person.name,
            'gas' : self.resource.gas,
        }

    def _get_edit_form_class(self):
        """Return edit form class. Usually a FormFromModel"""
        return EditGASMemberForm

