from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction
from gasistafelice.consts import CREATE, EDIT, EDIT_MULTIPLE, VIEW

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response

from gasistafelice.gas.models.base import GAS, GASMember
from gasistafelice.supplier.models import Supplier
from gasistafelice.gas.forms.order.plan import SingleGASMemberPlanedOrderForm, AddPlanedOrderForm

from flexi_auth.models import ObjectWithContext

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "planed_orders"
    BLOCK_DESCRIPTION = _("Planed Orders")
    BLOCK_VALID_RESOURCE_TYPES = ["gasmember"] 

    COLUMN_INDEX_NAME_MAP = { 
        0: 'pk',
        1: 'gasstock__product__name',
        2: 'gasstock__name',
        3: 'planed_amount',
        4: 'is_suspended'
    }

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
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE, verbose_name=_("Add"), 
                    popup_form=True,
                    method="get",
                ),
            ]

        return user_actions
        
    def _get_resource_list(self, request):
        # SupplierStock list
        return request.resource.planedstocks

    def _get_add_form_class(self):
        return AddPlanedOrderForm

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        data = {}
        i = 0
        
        for i,el in enumerate(querySet):
            key_prefix = 'form-%d' % i
            data.update({
               '%s-id' % key_prefix : el.pk,
               '%s-pk' % key_prefix : el.pk,
               '%s-supplier' % key_prefix : el.gasstock.supplier,
               '%s-product' % key_prefix : el.gasstock.product.name,
               '%s-planed_amount' % key_prefix : el.planed_amount,
               '%s-availability' % key_prefix : el.is_suspended,
            })
        
        data['form-TOTAL_FORMS'] = i + 1  #empty form for create new insert data
        data['form-INITIAL_FORMS'] = 0
        data['form-MAX_NUM_FORMS'] = 0

        formset = SingleGASMemberPlanedOrderForm(request, data)

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
                'supplier' : querySet[i].gasstock.supplier,
                'product' : form['product'],
                'planed_amount' : form['planed_amount'],
                'availability' : form['availability'],
            })

        return formset, records, {}

    def _get_edit_multiple_form_class(self):
        return SingleGASMemberPlanedOrderForm

