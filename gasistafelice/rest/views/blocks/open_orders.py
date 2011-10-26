from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers
from django.contrib.auth.models import User

from flexi_auth.models import ObjectWithContext

from gasistafelice.rest.views.blocks.base import BlockWithList, Action, ResourceBlockAction
from gasistafelice.consts import CREATE, EDIT
from gasistafelice.gas.forms import order as order_forms
from gasistafelice.gas.models import GASSupplierOrder, GASSupplierSolidalPact

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "open_orders"
    BLOCK_DESCRIPTION = _("Open orders")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "supplier", "gas", "pact"] 

    TEMPLATE_RESOURCE_LIST = "blocks/open_orders.xml"

    def _get_add_form_class(self):
        return order_forms.form_class_factory_for_request(self.request, base=order_forms.AddOrderForm)

    def _get_resource_list(self, request):
        return request.resource.orders.open()

    def _get_user_actions(self, request):

        user_actions = []

        # TODO: refactory needed, has_perm check needed
        rt = self.resource.resource_type
        perm = False
        if rt is not "site":
            perm = request.user in self.resource.des.referrers

        #if request.user.has_perm(CREATE, 
        #    obj=ObjectWithContext(GASSupplierOrder, context={'pact': request.resource.pact})):
        # Cannot retrieve pact from "site", "supplier" nor "gas"
        # FIXME: TODO: PATCH:

        if not perm:
            # TODO: Ci piacerebbe che se uno e' un referente di _almeno un_ fornitore 
            # TODO: ha il pulsante "aggiugni ordine"
            # TODO: poi le scelte saranno limitate ai suoi diritti nel popup
            if rt in ["gas","pact"]:
                perm = request.user in self.resource.referrers | self.resource.gas.referrers
            elif rt == "supplier":
                # TODO: following code works, but, in order to make "add order" work
                # we have to implement supplier.forms.order.SupplierAddOrderForm
                return []
#                refs = User.objects.none()
#                for p in self.resource.pacts:
#                    refs |= p.referrers
#                    refs |= p.gas.referrers
#                perm = request.user in refs


        if perm is True:
            user_actions += [
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE, verbose_name=_("Add order"), 
                    popup_form=True
                ),
             ]

        return user_actions

