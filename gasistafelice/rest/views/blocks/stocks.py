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

    BLOCK_NAME = "stocks"
    BLOCK_DESCRIPTION = _("Stocks")
    BLOCK_VALID_RESOURCE_TYPES = ["supplier"] 

    COLUMN_INDEX_NAME_MAP = { 
        0: 'pk',
        1: 'code', 
        2: 'product', 
        3: 'product__description', 
        4: 'price', 
        5: 'availability' 
    }

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(EDIT, obj=request.resource):
            user_actions += [
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=VIEW, verbose_name=_("Show stock"), 
                    popup_form=False,
                    method="get",
                ),
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=EDIT_MULTIPLE, verbose_name=_("Edit stock"), 
                    popup_form=False,
                    method="get",
                ),
            ]

        return user_actions
        
    def _get_resource_list(self, request):
        return request.resource.stocks

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        # Build a dict (should be a QueryDict) with data needed for FormSet initialization

        data = {}
        for i,el in enumerate(querySet):
            key_prefix = 'form-%d' % i
            data.update({
               '%s-id' % key_prefix : el.pk,
               '%s-code' % key_prefix : el.code,
               '%s-product' % key_prefix : el.product,
               '%s-price' % key_prefix : floatformat(el.price, 2),
               '%s-availability' % key_prefix : el.amount_available,
            })

        data['form-TOTAL_FORMS'] = i
        data['form-INITIAL_FORMS'] = 0
        data['form-MAX_NUM_FORMS'] = 0

        formset = SingleSupplierStockFormSet(request, data)

        records = []
        c = querySet.count()
        for i,form in enumerate(formset):

            if i < c:
                description = querySet[i].product.description
                pk = querySet[i].pk
            else:
                description = ""
                pk = None

            records.append({
                'id' : form['id'],
                'code' : form['code'],
                'product' : form['product'],
                'description' : description,
                'price' : form['price'],
                'availability' : form['availability'],
            })

        return formset, records

    def _get_edit_multiple_form_class(self):
        return SingleSupplierStockFormSet

