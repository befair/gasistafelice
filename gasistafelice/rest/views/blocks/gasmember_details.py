"""View for block details specialized for a GAS"""

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from gasistafelice.rest.views.blocks import details

class Block(details.Block):

    BLOCK_NAME = "gasmember_details"
    BLOCK_VALID_RESOURCE_TYPES = ["gasmember"] 

    def _get_user_actions(self, request):

        return []
