from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction, CREATE_PDF, SENDME_PDF
from gasistafelice.consts import EDIT, CONFIRM

from gasistafelice.lib.shortcuts import render_to_response, render_to_context_response
from gasistafelice.lib.http import HttpResponse

from gasistafelice.gas.models import GASMember

from gasistafelice.gas.forms.order.gmo import BasketGASMemberOrderForm
from gasistafelice.lib.formsets import BaseFormSetWithRequest
from django.forms.formsets import formset_factory

import cgi, os

import logging
log = logging.getLogger(__name__)

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "basket"
    BLOCK_DESCRIPTION = _("Basket")
    BLOCK_VALID_RESOURCE_TYPES = ["gasmember"]

        #3: 'ordered_product__stock__supplier_stock__product', gasstock
    COLUMN_INDEX_NAME_MAP = {
        0: 'pk',
        1: 'ordered_product__order__pk',
        2: 'ordered_product__gasstock__stock__supplier__name',
        3: 'ordered_product__gasstock__stock__product__name',
        4: 'ordered_price',
        5: '' ,
        6: 'ordered_amount',
        7: 'tot_price',
        8: 'enabled',
        9: ''
    }
#,
#        10: ''  --> order_urn

    def _get_user_actions(self, request):

        user_actions = []

        if not request.resource.gas.config.gasmember_auto_confirm_order:

            #TODO seldon: does this work for a GASMember?
            #if request.user.has_perm(EDIT, obj=request.resource):
            if request.user == request.resource.person.user:
                user_actions += [
                    ResourceBlockAction( 
                        block_name = self.BLOCK_NAME,
                        resource = request.resource,
                        name=CONFIRM, verbose_name=_("Confirm all"),
                        popup_form=False,
                    ),

                ]

        if request.user == request.resource.person.user:

            user_actions += [
                ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE_PDF, verbose_name=_("Create PDF"),
                    popup_form=False,
                ),
                ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=SENDME_PDF, verbose_name=_("Send email PDF gasmember"),
                    popup_form=False,
                )
            ]

        return user_actions
        
    def _get_resource_list(self, request):
        #qs = request.resource.basket | request.resource.basket_to_be_delivered
        qs = request.resource.basket
        return qs


    def _get_edit_multiple_form_class(self):
        qs = self._get_resource_list(self.request)
        return formset_factory(
                    form=BasketGASMemberOrderForm,
                    formset=BaseFormSetWithRequest, 
                    extra=qs.count()
        )


    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        gmos = querySet

        data = {}
#        data2 = {}
        i = 0
        c = gmos.count()
        
        # Store mapping between GSSOP-id and neededs info: formset_index and ordered_total
        map_info = { }

        gmo =  self.resource #GASMemberOrder()
        av = False

        for i,el in enumerate(querySet):

            key_prefix = 'form-%d' % i
            data.update({
               '%s-id' % key_prefix : el.pk, #gmo.pk,
               '%s-ordered_amount' % key_prefix : el.ordered_amount or 0,
               '%s-ordered_price' % key_prefix : el.ordered_product.order_price, #displayed as hiddend field
               '%s-gm_id' % key_prefix : gmo.pk, #displayed as hiddend field !Attention is gmo_id 
               '%s-gsop_id' % key_prefix : el.ordered_product.pk,
               '%s-enabled' % key_prefix : bool(av),
            })

            map_info[el.pk] = {
                'formset_index' : i,
                'ordered_total' : el.tot_price, # This is the total computed NOW (with ordered_product.price)
            }

        data['form-TOTAL_FORMS'] = c
        data['form-INITIAL_FORMS'] = c
        data['form-MAX_NUM_FORMS'] = 0

        formset = self._get_edit_multiple_form_class()(request, data)

        records = []

        for i,el in enumerate(querySet):
            form = formset[map_info[el.pk]['formset_index']]
            total = map_info[el.pk]['ordered_total']

            form.fields['ordered_amount'].widget.attrs = { 
                'class' : 'amount',
                'step' : el.ordered_product.gasstock.step or 1,
                'minimum_amount' : el.ordered_product.gasstock.minimum_amount or 1,
                'eur_chan' : ["", "alert"][bool(el.has_changed)],
                'req_conf' : ["alert", ""][bool(el.is_confirmed)],
                's_url' : el.supplier.urn,
                'p_url' : el.stock.urn,
            }
                #'p_url' : el.product.urn,

            records.append({
               'id' : "%s %s %s %s %s" % (el.pk, form['id'], form['gm_id'], form['gsop_id'], form['ordered_price']),
               'order' : el.order.pk,
               'supplier' : el.supplier,
               'product' : el.product,
               'price' : el.ordered_product.order_price,
               'price_changed' : not el.has_changed,
               'ordered_amount' : form['ordered_amount'], #field inizializzato con il minimo amount e che ha l'attributo step
               'ordered_total' : total,
               'field_enabled' : form['enabled'],
               'order_confirmed' : el.is_confirmed,
               'order_urn' : el.order.urn,
            })
               #'description' : el.product.description,

        #return records, records, {}
        return formset, records, {}


    def _set_records(self, request, records):
        pass

    def get_response(self, request, resource_type, resource_id, args):

        try:
            rv = super(Block, self).get_response(request, resource_type, resource_id, args)
        except NotImplementedError:
            # Not implemented args are implemented in this method
            pass

        if args == CONFIRM:
            for gmo in self.resource.basket:
                log.debug(u"Sto confermando un ordine gasista(%s)" % gmo)
                gmo.confirm()
                gmo.save()

            #IMPORTANT: unset args to compute table results!
            args = self.KW_DATA

        elif args == CREATE_PDF:
            rv = self._create_pdf()
        elif args == SENDME_PDF:
            rv = self._send_email_logged()
        
        #TODO FIXME: ugly patch to fix AFTERrecords.append( 6
        if args == self.KW_DATA:
            from gasistafelice.lib.views_support import prepare_datatables_queryset, render_datatables
            
            querySet = self._get_resource_list(request) 
            #columnIndexNameMap is required for correct sorting behavior
            columnIndexNameMap = self.COLUMN_INDEX_NAME_MAP
            #path to template used to generate json (optional)
            jsonTemplatePath = 'blocks/%s/data.json' % self.BLOCK_NAME

            querySet, dt_params = prepare_datatables_queryset(request, querySet, columnIndexNameMap)
            #TODO FIXME: AFTER 6 
            formset, records, moreData = self._get_records(request, querySet)
            rv = render_datatables(request, records, dt_params, jsonTemplatePath)

        return rv


    def _send_email_logged(self):
        try:
            #WAS: to = self.request.user.email
            #WAS: self.resource.send_email([to],None, 'Order Email me', self.request.user)
            self.resource.send_email_to_gasmember(None, 'Order Email me', self.request.user)
            return self.response_success()
        except Exception, e:
            return self.response_error(_('We had some errors<pre>%s</pre>') % cgi.escape(e))

    def _create_pdf(self):

        pdf_data = self.resource.get_pdf_data(requested_by=self.request.user)

        if not pdf_data:
            rv = self.response_error(_('Report not generated')) 
        else:
            response = HttpResponse(pdf_data, mimetype='application/pdf')
            response['Content-Disposition'] = "attachment; filename=" + self.resource.get_valid_name() + ".pdf" 
            rv = response
        return rv



