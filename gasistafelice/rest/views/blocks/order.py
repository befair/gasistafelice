from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction, CREATE_PDF
from gasistafelice.consts import CREATE, EDIT, EDIT_MULTIPLE, VIEW

from gasistafelice.lib.shortcuts import render_to_xml_response, render_to_context_response

from gasistafelice.supplier.models import Supplier
from gasistafelice.gas.models import GASMemberOrder
from gasistafelice.gas.forms.order import SingleGASMemberOrderForm, BaseFormSetWithRequest, formset_factory
import logging
log = logging.getLogger(__name__)


#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "order"
    BLOCK_DESCRIPTION = _("Order")
    BLOCK_VALID_RESOURCE_TYPES = ["gasmember"] 

    COLUMN_INDEX_NAME_MAP = {
        0: 'order__pk', 
        1: 'gasstock__stock__supplier__name', 
        2: 'gasstock__stock__product__name',
        3: '',
        4: 'order_price',
        5: 'tot_amount',
        6: 'tot_price',
    }
#        3: 'gasstock__stock__product__description',

    def _get_resource_list(self, request):
        selected_orders = request.GET.getlist('gfCP_order')
        rv = request.resource.orderable_products
        if (selected_orders):
            rv = rv.filter(order__pk__in=map(int, selected_orders))
        return rv

    def options_response(self, request, resource_type, resource_id):
        """Get options for orders block. Check GAS configuration.
        WARNING: call to this method doesn't pass through get_response
        so you have to reset self.request and self.resource attribute if you want
        """

        self.request = request
        self.resource = request.resource

        gas = self.resource.gas

        orders = gas.orders.open()
        field_type = "checkbox"

        if gas.config.order_show_only_next_delivery:
            orders = orders.order_by('-delivery__date')
            if orders[0].delivery:
                orders.filter(delivery__date=orders[0].delivery.date)
            else:
                orders.filter(delivery__date__isnull=True)

        elif gas.config.order_show_only_one_at_a_time:
            field_type = "radio"

        fields = []
    
        for i,open_order in enumerate(orders):
            if field_type == "radio":
                selected = i == 0
            else:
                selected = True
        
            fields.append({
                'field_type'   : field_type,
                'field_label'  : open_order,
                'field_name'   : 'order',
                'field_values' : [{ 'value' : open_order.pk, 'selected' : selected}]
            }) 

        ctx = {
            'block_name' : self.description,
            'fields': fields,
        }
        return render_to_xml_response('options.xml', ctx)

        
    def _get_edit_multiple_form_class(self):

        qs = self._get_resource_list(self.request)

        return formset_factory(
                    form=SingleGASMemberOrderForm,
                    formset=BaseFormSetWithRequest, 
                    extra=qs.count() - self.__get_gmos(qs).count()
        )

    def __get_gmos(self, gssop):
        return GASMemberOrder.objects.filter(
                    ordered_product__in=gssop,
                    purchaser=self.request.resource.gasmember
        )

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        # [:] forces evaluation of the querySet
        gmos = self.__get_gmos(querySet)[:]

        data = {}
        i = 0
        c = querySet.count()
        
        # Store mapping between GSSOP-id and neededs info: formset_index and ordered_total
        gmo_info = { }

        gmo_lint = GASMemberOrder()

        for i,el in enumerate(querySet):

            try:
                #TODO: to be improved in performance
                gmo = el.gasmember_order_set.get(
                        purchaser=self.request.resource.gasmember
                )
            except GASMemberOrder.DoesNotExist:
                gmo=gmo_lint

            key_prefix = 'form-%d' % i
            data.update({
               '%s-id' % key_prefix : gmo.pk,
               '%s-ordered_amount' % key_prefix : gmo.ordered_amount or 0,
               '%s-ordered_price' % key_prefix : el.gasstock.price, #displayed as hiddend field
               '%s-gssop_id' % key_prefix : el.pk, #displayed as hiddend field
               '%s-note' % key_prefix : gmo.note,
            })

            gmo_info[el.pk] = {
                'formset_index' : i,
                'ordered_total' : (el.gasstock.price or 0)*(gmo.ordered_amount or 0), # This is the total computed NOW (with ordered_product.price)
            }


        data['form-TOTAL_FORMS'] = c 
        data['form-INITIAL_FORMS'] = gmos.count()
        data['form-MAX_NUM_FORMS'] = 0

        formset = self._get_edit_multiple_form_class()(request, data)

        records = []

        for i,el in enumerate(querySet):
            #log.debug("order ordered_amount (%s)" % (i))
            try:
                form = formset[gmo_info[el.pk]['formset_index']]
                total = gmo_info[el.pk]['ordered_total']
            except KeyError:
                # GASMember has not ordered this product: build an empty form
                form = SingleGASMemberOrderForm(self.request)
                total = 0

            #try:
            form.fields['ordered_amount'].widget.attrs = { 
                            'class' : 'amount',
                            'step' : el.gasstock.step or 1,
                            'minimum_amount' : el.gasstock.minimum_amount or 1,
                            's_url' : el.supplier.urn,
                            'p_url' : el.product.urn,
            }

            records.append({
               'id' : "%s %s %s %s" % (el.pk, form['id'], form['gssop_id'], form['ordered_price']),
               'supplier' : el.supplier,
               'product' : el.product,
               'note' : form['note'],
               'price' : el.gasstock.price,
               'ordered_amount' : form['ordered_amount'], #field inizializzato con il minimo amount e che ha l'attributo step
               'ordered_total' : total
            })
               #'description' : el.product.description,
            #except KeyError:
            #    log.debug("order ordered_amount (%s %s)" % (el.pk, i))

        return formset, records, {}

