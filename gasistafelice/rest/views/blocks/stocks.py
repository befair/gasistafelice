from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction
from gasistafelice.consts import CREATE, EDIT, EDIT_MULTIPLE, VIEW

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response

from gasistafelice.supplier.models import Supplier
from gasistafelice.supplier.forms import SingleSupplierStockFormSet

from flexi_auth.models import ObjectWithContext

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "stocks"
    BLOCK_DESCRIPTION = _("Stocks")
    BLOCK_VALID_RESOURCE_TYPES = ["supplier"] 

    COLUMN_INDEX_NAME_MAP = { 
        0: 'pk',
        1: 'product',
        2: 'product__description',
        3: 'price',
        4: 'availability'
    }
        #1: 'stock',
        #1: 'code',

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(EDIT, obj=ObjectWithContext(request.resource)):
            user_actions += [
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=VIEW, verbose_name=_("Show"), 
                    popup_form=False,
                    method="get",
                ),
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=EDIT_MULTIPLE, verbose_name=_("Edit"), 
                    popup_form=False,
                    method="get",
                ),
            ]

        return user_actions
        
    def _get_resource_list(self, request):
        # SupplierStock list
        return request.resource.stocks

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        # Build a dict (should be a QueryDict) with data needed for FormSet initialization

        data = {}
        i = 0
        
        for i,el in enumerate(querySet):
            key_prefix = 'form-%d' % i
            data.update({
               '%s-id' % key_prefix : el.pk,
               '%s-pk' % key_prefix : el.pk,
               '%s-product' % key_prefix : el.product.name,
               '%s-description' % key_prefix : el.product.description,
               '%s-price' % key_prefix : el.price,
               '%s-availability' % key_prefix : el.amount_available,
            })
               #'%s-stock_regex' % key_prefix : el,
               #'%s-code' % key_prefix : el.code,

        data['form-TOTAL_FORMS'] = i + 1  #empty form for create new insert data
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
                'id' : "%s %s" % (form['pk'], form['id']),
                'product' : form['product'],
                'description' : form['description'], #description,
                'price' : form['price'],
                'availability' : form['availability'],
            })
                #'stock' : form['stock_regex'],
                #'code' : form['code'],

        return formset, records, {}

    def _get_edit_multiple_form_class(self):
        return SingleSupplierStockFormSet

