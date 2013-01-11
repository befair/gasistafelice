from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers
from django.contrib.auth.models import User
from django.http import HttpResponse

from flexi_auth.models import ObjectWithContext

from gasistafelice.rest.views.blocks.base import BlockWithList, ResourceBlockAction
from gasistafelice.consts import CREATE, EDIT
from gasistafelice.gas.forms import order as order_forms
from gasistafelice.gas.models import GASSupplierOrder

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "open_orders"
    BLOCK_DESCRIPTION = _("Open orders")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas", "supplier", "pact", "stock"] 

    TEMPLATE_RESOURCE_LIST = "blocks/open_orders.xml"

    def _get_add_form_class(self):
        """Dynamic generation of order add form basing on GASConfig.

        For choosing base class keep in consideration GASConfig options
        """

        t = self.resource.resource_type
        if t in ["site", "supplier"]:
            base_class = order_forms.AddOrderForm
        elif t in ["gas", "pact"]:
            gas = self.resource.gas
            if gas.config.use_order_planning:
                if gas.config.intergas_connection_set.count():
                    base_class = order_forms.AddInterGASPlannedOrderForm
                else:
                    base_class = order_forms.AddPlannedOrderForm
            else:
                if gas.config.intergas_connection_set.count():
                    base_class = order_forms.AddInterGASOrderForm
                else:
                    base_class = order_forms.AddOrderForm
        else:
            raise ValueError("Invalid block %s for a %s" % (self.BLOCK_NAME, t))

        return order_forms.form_class_factory_for_request(
            self.request, base=base_class
        )

    def _get_resource_list(self, request):
        orders = request.resource.orders.open()
        for order in orders:
            order.order_url = order.get_absolute_url_order_page_for_user(request.user)
        return orders

    def _get_user_actions(self, request):

        user_actions = []
        ctx = { self.resource.resource_type : self.resource }

        if request.user.has_perm(CREATE, 
            obj=ObjectWithContext(GASSupplierOrder, context=ctx)
        ):
        
            if self.resource.resource_type in ["gas", "supplier", "pact"]:
                user_actions += [
                    ResourceBlockAction( 
                        block_name = self.BLOCK_NAME,
                        resource = request.resource,
                        name=CREATE, verbose_name=_("Add order"),
                        popup_form=True
                    ),
                 ]

        return user_actions


    def get_response(self, request, resource_type, resource_id, args):

        self.request = request
        self.resource = resource = request.resource

        if not resource.pacts:

            msg = _("There are no pacts related to this %s, no order can exist") % resource_type
            return HttpResponse('<root><sysmsg>%s</sysmsg></root>' % msg)

        return super(Block, self).get_response(request, resource_type, resource_id, args)

