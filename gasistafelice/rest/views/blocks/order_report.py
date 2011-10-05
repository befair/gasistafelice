from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction, CREATE_PDF
from gasistafelice.consts import CREATE, EDIT, EDIT_MULTIPLE, VIEW

from gasistafelice.lib.shortcuts import render_to_xml_response, render_to_context_response

from gasistafelice.supplier.models import Supplier
from gasistafelice.gas.forms.order import GASSupplierOrderProductFormSet
from django.template.defaultfilters import floatformat

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import cgi, os
from django.conf import settings

from django.utils.encoding import smart_unicode

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "order_report"
    BLOCK_DESCRIPTION = _("Order report")
    BLOCK_VALID_RESOURCE_TYPES = ["order"] 

    COLUMN_INDEX_NAME_MAP = {
        0: 'gasstock__stock__product',
        1: 'gasstock__stock__price', 
        2: 'tot_gasmembers',
        3: 'tot_amount',
        4: 'tot_price',
        5: 'enabled' 
    }

    def _get_user_actions(self, request):
  
        user_actions = []

        # Check if order is in "closed_state"
        user_actions = [

                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE_PDF, verbose_name=_("Create PDF"), 
                    popup_form=False,
                ),
        ]

        return user_actions

    def _get_resource_products(self, request):
        # Maybe we need to switch args KW_DATA, or EDIT_MULTIPLE
        # to get GASSupplierOrderProduct or GASSupplierStock respectively
        return request.resource.orderable_products

    def _get_resource_families(self, request):
        return request.resource.ordered_products

    def _get_edit_multiple_form_class(self):
        return GASSupplierOrderProductFormSet

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

#        data = {}
#        i = 0
#        
#        for i,el in enumerate(querySet):
#
#            key_prefix = 'form-%d' % i
#            data.update({
#               '%s-id' % key_prefix : el.pk,
#               '%s-enabled' % key_prefix : True,
#            })
#
#        data['form-TOTAL_FORMS'] = i 
#        data['form-INITIAL_FORMS'] = 0
#        data['form-MAX_NUM_FORMS'] = 0
#
#        formset = GASSupplierOrderProductFormSet(request, data)
#
#        records = []
#        c = querySet.count()
        for i,el in enumerate(querySet):

            records.append({
               'product' : el.product,
               'price' : floatformat(el.order_price, 2),
               'tot_gasmembers' : el.tot_gasmembers,
               'tot_amount' : el.tot_amount,
               'tot_price' : el.tot_price,
#               'field_enabled' : "%s %s" % (form['id'], form['enabled']),

            })

        return None, records, {}


    def _get_pdfrecords_products(self, querySet):
        """Return records of rendered table fields."""

        records = []
        c = querySet.count()

        for el in querySet:
            if el.tot_price > 0:
                records.append({
                   'product' : el.product.name.encode('utf-8', "ignore"), #.replace(u'\u2019', '\'').decode('latin-1'),
                   'price' : el.order_price,
                   'tot_gasmembers' : el.tot_gasmembers,
                   'tot_amount' : el.tot_amount,
                   'tot_price' : el.tot_price,
                })

        return records

    def _get_pdfrecords_families(self, querySet):
        """Return records of rendered table fields."""

        records = []
        #memorize family, total price and number of products
        subTotals = []
        actualFamily = -1
        loadedFamily = -1
        rowFam = -1
        description = ""
        product = ""
        tot_fam = 0
        nProducts = 0
        tot_Ord = 0

        for el in querySet:
            rowFam = el.purchaser.pk
            if actualFamily == -1 or actualFamily != rowFam:
                if actualFamily != -1:
                    subTotals.append({
                       'family_id' : actualFamily,
                       'gasmember' : description,
                       'basket_price' : tot_fam,
                       'basket_products' : nProducts,
                    })
                    tot_fam = 0
                    nProducts = 0
                actualFamily = rowFam
                description = smart_unicode(el.purchaser.person)
            product = smart_unicode(el.product)

            tot_fam += el.tot_price
            nProducts += 1
            tot_Ord += el.tot_price

            records.append({
               'product' : product,
               'price_ordered' : el.ordered_price,
               'price_delivered' : el.ordered_product.order_price,
               'price_changed' : el.has_changed,
               'amount' : el.ordered_amount,
               'tot_price' : el.tot_price,
               'family_id' : rowFam,
            })

        if actualFamily != -1 and tot_fam > 0:
            subTotals.append({
               'family_id' : actualFamily,
               'gasmember' : description,
               'basket_price' : tot_fam,
               'basket_products' : nProducts,
            })

        return records, tot_Ord, subTotals


    def get_response(self, request, resource_type, resource_id, args):

        self.request = request
        self.resource = resource = request.resource

        if args == CREATE_PDF:
            return self._create_pdf()
        else:
            return super(Block, self).get_response(request, resource_type, resource_id, args)


    def _create_pdf(self):

        # Dati di esempio
        order = self.resource.order
        fams, total_calc, subTotals = self._get_pdfrecords_families(self._get_resource_families(self.request).order_by('purchaser__person__name'))
        context_dict = {
            'order' : order,
            'recProd' : self._get_pdfrecords_products(self._get_resource_products(self.request).filter(gasmember_order_set__ordered_amount__gt=0).distinct()), 
            'recFam' : fams, 
            'subFam' : subTotals, 
            'user' : self.request.user,
            'total_amount' : self.resource.tot_price, #total da Model
            'total_calc' : total_calc, #total dal calcolato
        }

        REPORT_TEMPLATE = "blocks/%s/report.html" % self.BLOCK_NAME

        template = get_template(REPORT_TEMPLATE)
        context = Context(context_dict)
        html = template.render(context)
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1", "ignore")), result)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), mimetype='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=GAS_%s_%s.pdf' % \
                            (order.supplier, '20110909')
#                            (order.supplier, '{0:%Y%m%d}'.format(order.delivery.date))
            return response
        return HttpResponse(_('We had some errors<pre>%s</pre>') % cgi.escape(html))
