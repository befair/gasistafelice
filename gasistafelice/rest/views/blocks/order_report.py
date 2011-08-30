from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction
from gasistafelice.auth import CREATE, EDIT, EDIT_MULTIPLE, VIEW

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response

from gasistafelice.supplier.models import Supplier
from gasistafelice.supplier.forms import SingleSupplierStockFormSet
from django.template.defaultfilters import floatformat

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "order_report"
    BLOCK_DESCRIPTION = _("Order report")
    BLOCK_VALID_RESOURCE_TYPES = ["order"] 

    COLUMN_INDEX_NAME_MAP = { 0: 'code', 1 : 'product', 2: 'product__description', 3: 'price', 4: 'availability' }

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(EDIT, obj=request.resource):
            user_actions += [
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=VIEW, verbose_name=_("Show stock"), 
                    popup_form=False,
                ),
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=EDIT_MULTIPLE, verbose_name=_("Edit stock"), 
                    popup_form=False,
                ),
            ]

        return user_actions
        
    def _get_resource_list(self, request):
        return request.resource.stocks

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        formset_initial = []

        for el in querySet:
           formset_initial.append({
               'code' : el.code,
               'product' : el.product,
               'price' : floatformat(el.price, 2),
               'availability' : el.availability,
            })

        formset = SingleSupplierStockFormSet(initial=formset_initial)

        records = []
        c = querySet.count()

        for i,form in enumerate(formset):

            if i < c:
                description = querySet[i].product.description
            else:
                description = ""

            records.append({
                'code' : form['code'],
                'product' : form['product'],
                'description' : description,
                'price' : form['price'],
                'availability' : form['availability'],
            })

        return records

    def _set_records(self, request, records):
        pass
