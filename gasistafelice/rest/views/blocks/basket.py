from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction, CREATE_PDF
from gasistafelice.consts import EDIT, CONFIRM

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response
from gasistafelice.lib.http import HttpResponse

from django.template.defaultfilters import floatformat

from gasistafelice.gas.models import GASMember
from django.template.defaultfilters import floatformat

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import cgi, os
from django.conf import settings
from datetime import datetime

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "basket"
    BLOCK_DESCRIPTION = _("Basket")
    BLOCK_VALID_RESOURCE_TYPES = ["gasmember"] 

    COLUMN_INDEX_NAME_MAP = { 
        0: 'ordered_product__order__pk', 
        1: 'ordered_product__gasstock__stock__supplier', 
        2: 'ordered_product__stock__supplier_stock__product', 
        3: 'ordered_amount', 
        4: 'ordered_price', 
        5: 'tot_price', 
        6: '' 
    }

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

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        records = []
        c = querySet.count()

        for el in querySet:

            records.append({
               'order' : el.ordered_product.order.pk,
               'supplier' : el.ordered_product.stock.supplier,
               'product' : el.product,
               'amount' : floatformat(el.ordered_amount, "-2"),
               'price' : floatformat(el.ordered_product.order_price, 2),
               'price_changed' : el.has_changed,
               'tot_price' : floatformat(el.tot_price, 2),
            })
               #'price' : floatformat(el.ordered_product.gasstock.price, 2),

        return records, records, {}

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

               #'product' : el.product.encode('utf-8', "ignore"),
            records.append({
               'order' : rowOrder,
               'order_description' : description,
               'supplier' : producer,
               'amount' : floatformat(el.ordered_amount, "-2"),
               'price_ordered' : floatformat(el.ordered_price, 2),
               'price_delivered' : floatformat(el.ordered_product.order_price, 2),
               'price_changed' : el.has_changed,
               'tot_price' : floatformat(el.tot_price, 2),
               'tot_prod' : tot_prod,
               'order_confirmed' : el.is_confirmed,
            })

        return records


    def _set_records(self, request, records):
        pass

    def get_response(self, request, resource_type, resource_id, args):

        self.resource = request.resource
        self.request = request

        if args == CONFIRM:
            for gmo in resource.basket:
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
        querySet = self._get_resource_list(self.request)
        context_dict = {
            'gasmember' : gasmember,
            'records' : self._get_pdfrecords(self.request, querySet),
            'rec_count' : querySet.count(),
            'user' : self.request.user,
            'total_amount' : floatformat(self.resource.total_basket, 2),
            'CSS_URL' : settings.MEDIA_ROOT,
        }

        REPORT_TEMPLATE = "blocks/%s/report.html" % self.BLOCK_NAME

        template = get_template(REPORT_TEMPLATE)
        context = Context(context_dict)
        html = template.render(context)
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), mimetype='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=GASMember_%s_%s.pdf' % \
                            (gasmember.id_in_gas, '{0:%Y%m%d_%H%M}'.format(datetime.now()))
            return response
        return HttpResponse(_('We had some errors<pre>%s</pre>') % cgi.escape(html))
