from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from flexi_auth.models import ObjectWithContext

from rest.views.blocks.base import BlockWithList, ResourceBlockAction
from consts import CREATE
from gf.gas.models.base import GASSupplierSolidalPact

from rest.views.blocks import pacts
#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(pacts.Block):

    BLOCK_NAME = "des_pacts"
    BLOCK_VALID_RESOURCE_TYPES = ["site"]

    def _get_resource_list(self, request):
        return request.resource.pacts

    def _get_user_actions(self, request):

        user_actions = []

        #TODO: there should be a DES presentation for adding a pact in DES
        return user_actions
        
    def _get_add_form_class(self):

        ct_name = self.resource.__class__.__name__
        raise NotImplementedError("No add form for GASSupplierSolidalPact within a %s" % ct_name)

