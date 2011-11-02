from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from flexi_auth.models import ObjectWithContext

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction, CREATE_PDF
from gasistafelice.consts import EDIT, CONFIRM

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response
from gasistafelice.lib.http import HttpResponse

from gasistafelice.gas.models import GASMember

from gasistafelice.gas.forms.order import BasketGASMemberOrderForm, SingleGASMemberOrderForm, BaseFormSetWithRequest, formset_factory

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import cgi, os
from django.conf import settings
from datetime import datetime
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
        2: 'ordered_product__gasstock__stock__supplier', 
        3: 'ordered_product__gasstock__stock__product', 
        4: 'ordered_price', 
        5: '' ,
        6: 'ordered_amount', 
        7: 'tot_price', 
        8: 'enabled' ,
        9: '' 
    }

    def _get_user_actions(self, request):

        user_actions = []

        if request.resource.gas.config.gasmember_auto_confirm_order:

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
        user_actions += [
            ResourceBlockAction( 
                block_name = self.BLOCK_NAME,
                resource = request.resource,
                name=CREATE_PDF, verbose_name=_("Create PDF"), 
                popup_form=False,
            ),
        ]

        return user_actions
        
    def _get_resource_list(self, request):
        return request.resource.basket


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
                            'p_url' : el.product.urn,
            }

            records.append({
               'id' : "%s %s %s %s %s" % (el.pk, form['id'], form['gm_id'], form['gsop_id'], form['ordered_price']),
               'order' : el.ordered_product.order.pk,
               'supplier' : el.supplier,
               'product' : el.product,
               'price' : el.ordered_product.order_price,
               'price_changed' : not el.has_changed,
               'ordered_amount' : form['ordered_amount'], #field inizializzato con il minimo amount e che ha l'attributo step
               'ordered_total' : total,
               'field_enabled' : form['enabled'],
               'order_confirmed' : el.is_confirmed,
            })
               #'description' : el.product.description,

        #return records, records, {}
        return formset, records, {}



    def _get_pdfrecords(self, request, querySet):
        """Return records of rendered table fields."""

        records = []
        actualProduttore = -1
        rowOrder = -1
        description = ""
        producer = ""
        tot_prod = 0

        for el in querySet:
            rowOrder = el.ordered_product.order.pk
            if actualProduttore == -1 or actualProduttore != rowOrder:
                if actualProduttore != -1:
                    tot_prod = 0
                actualProduttore = rowOrder
                description = unicode(el.ordered_product.order)
                producer = el.ordered_product.stock.supplier
            tot_prod += el.tot_price

            records.append({
               'order' : rowOrder,
               'order_description' : description,
               'supplier' : producer,
               'amount' : el.ordered_amount,
               'product' : el.product,
               'price_ordered' : el.ordered_price,
               'price_delivered' : el.ordered_product.order_price,
               'price_changed' : el.has_changed,
               'tot_price' : el.tot_price,
               'tot_prod' : tot_prod,
               'order_confirmed' : el.is_confirmed,
               'note' : el.note,
            })

        return records


    def _set_records(self, request, records):
        pass

    def get_response(self, request, resource_type, resource_id, args):

        self.resource = request.resource
        self.request = request

        if args == CONFIRM:
            for gmo in self.resource.basket:
                log.debug("Sto confermando un ordine gassista(%s)" % gmo)
                gmo.confirm()

            #IMPORTANT: unset args to compute table results!
            args = self.KW_DATA
        elif args == CREATE_PDF:
            return self._create_pdf()
        
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
            return render_datatables(request, records, dt_params, jsonTemplatePath)

        return super(Block, self).get_response(request, resource_type, resource_id, args)

    def _create_pdf(self):

        gasmember = self.resource
        querySet = self._get_resource_list(self.request).order_by('ordered_product__order__pk')
        context_dict = {
            'gasmember' : gasmember,
            'records' : self._get_pdfrecords(self.request, querySet),
            'rec_count' : querySet.count(),
            'user' : self.request.user,
            'total_amount' : self.resource.total_basket,
            'CSS_URL' : settings.MEDIA_ROOT,
        }

        REPORT_TEMPLATE = "blocks/%s/report.html" % self.BLOCK_NAME

        template = get_template(REPORT_TEMPLATE)
        context = Context(context_dict)
        html = template.render(context)
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), mimetype='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=GASMember_%s_%s.pdf' % \
                            (gasmember.id_in_gas, '{0:%Y%m%d_%H%M}'.format(datetime.now()))
            return response
        return HttpResponse(_('We had some errors<pre>%s</pre>') % cgi.escape(html))
