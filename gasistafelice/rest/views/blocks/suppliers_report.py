from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction, CREATE_PDF
from gasistafelice.consts import CREATE, EDIT, EDIT_MULTIPLE, VIEW

from gasistafelice.lib.shortcuts import render_to_xml_response, render_to_context_response

from gasistafelice.supplier.models import Supplier
from gasistafelice.supplier.forms import SupplierForm
from gasistafelice.lib.formsets import BaseFormSetWithRequest
from django.forms.formsets import formset_factory

from django.http import HttpResponse
from django.template.loader import get_template
#from django.template.loader import render_to_string
from django.template import Context
#from django.template import RequestContext
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import cgi, os
from django.conf import settings
from gasistafelice.des.models import Siteattr

from django.utils.encoding import smart_unicode
from flexi_auth.models import ObjectWithContext

from gasistafelice.supplier.forms import AddSupplierForm

import logging
log = logging.getLogger(__name__)

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "suppliers_report"
    BLOCK_DESCRIPTION = _("Suppliers")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas"]

    COLUMN_INDEX_NAME_MAP = {
        0: 'pk',
        1: 'name',
        2: 'frontman__name',
        3: 'city',
        4: 'mail',
        5: 'phone',
        6: '',
        7: '',
        8: '',
        9: ''
    }

#        6: 'tot_stocks',
#        7: 'tot_pacts',
#        8: 'balance',
#        9: 'certifications_list'
#        10: 'enabled'

#Cannot resolve keyword '' into field. Choices are: agent_set, certifications, config, contact_set, description, flavour, frontman, gas, iban, id, logo, n_employers, name, pact_set, produced_product_set, seat, ssn, stock_set, supplieragent, supplierconfig, supplierproductcategory, vat_number, website


    def _get_user_actions(self, request):
  
        user_actions = []
        des = Siteattr.get_site()

        if request.user.has_perm(CREATE, \
            obj=ObjectWithContext(Supplier, context={'site':des})):

            user_actions.append( 
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE, verbose_name=_("Add supplier"), 
                    #WAS Supplier admin: url=urlresolvers.reverse('admin:supplier_supplier_add')
                )
            )

        user_actions += [
            ResourceBlockAction(
                block_name = self.BLOCK_NAME,
                resource = request.resource,
                name=CREATE_PDF, verbose_name=_("Create PDF"),
                popup_form=False,
            ),
        ]

# COMMENT fero: disabled because it does not work 
# COMMENT fero: (calls Supplier.product which is a no-sense, probably Supplier.products?)
# COMMENT fero: but also for needs to change SupplierForm in SingleSupplierForm (a row in formset)
#        if request.user.has_perm(EDIT, obj=ObjectWithContext(request.resource)):
#            user_actions += [
#                ResourceBlockAction(
#                    block_name = self.BLOCK_NAME,
#                    resource = request.resource,
#                    name=VIEW, verbose_name=_("Show"),
#                    popup_form=False,
#                    method="get",
#                ),
#                ResourceBlockAction(
#                    block_name = self.BLOCK_NAME,
#                    resource = request.resource,
#                    name=EDIT_MULTIPLE, verbose_name=_("Edit"),
#                    popup_form=False,
#                    method="get",
#                ),
#            ]
        return user_actions

    def _get_add_form_class(self):
        return AddSupplierForm

    def _get_resource_list(self, request):
        # Suppliers objects filtered without PRIVATE
        qry = request.resource.suppliers.order_by('name')
        #FIXME: change queryset into list
        #qry = filter(lambda t: not t.is_private, qry)
        return qry

    def _get_edit_multiple_form_class(self):
        qs = self._get_resource_list(self.request)
        return formset_factory(
                    form=SupplierForm,
                    formset=BaseFormSetWithRequest,
                    extra=qs.count()
        )

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        data = {}
        i = 0
        c = querySet.count()
        map_info = { }
        av = True

        for i,el in enumerate(querySet):

            key_prefix = 'form-%d' % i
            data.update({
               '%s-id' % key_prefix : el.pk, 
               '%s-enabled' % key_prefix : bool(av),
            })

            map_info[el.pk] = {'formset_index' : i}

        data['form-TOTAL_FORMS'] = c #i 
        data['form-INITIAL_FORMS'] = c #0
        data['form-MAX_NUM_FORMS'] = 0

        formset = self._get_edit_multiple_form_class()(request, data)

        records = []
        for i, el in enumerate(querySet):

            form = formset[map_info[el.pk]['formset_index']]

            records.append({
               'id' : el.pk,
               'product' : el.product,
               'price' : el.order_price,
               'price_changed' : el.has_changed,
               'tot_gasmembers' : el.tot_gasmembers,
               'unconfirmed' : el.unconfirmed_orders,
               'ordered_amount' : el.tot_amount,
               'ordered_total' : el.tot_price,
               'field_enabled' : "%s %s" % (form['id'], form['enabled']),
            })

        return formset, records, {}

    def _get_pdfrecords_pacts(self, querySet):
        """Return records of rendered table fields."""

        records = []
        #memorize pact, economic and number of products
        nSup = querySet.count()
        pact_count = 0
        nProducts = 0

        for el in querySet:
            pact_count += el.tot_pacts
            nProducts += el.tot_stocks

            records.append({
               'id' : el.pk,
               'name' : el.name,
               'frontman' : el.subject_name,   #frontman.report_name,
               'address' : el.address,
               'email' : el.preferred_email_address,
               'phone' : el.preferred_phone_address,
               'fax' : el.preferred_fax_address,
               'tot_stocks' : el.tot_stocks,
               'tot_pacts' : el.tot_pacts,
               'balance' : el.balance,
               'certs' : el.certifications_list,
            })

#            <td class="taright qta">{{row.tot_stocks|floatformat:"-2"}}</td>
#            <td class="taright qta">{{row.tot_pacts|floatformat:"-2"}}</td>
#            <td class="taright totprice">&nbsp;&euro;&nbsp;{{row.balance|floatformat:"2"}}</td>
#            <td>{{row.certs|escapejs}}</td>

        return records, nSup -3 , nProducts, pact_count


    def get_response(self, request, resource_type, resource_id, args):

        self.request = request
        self.resource = resource = request.resource

        if args == CREATE_PDF:
            return self._create_pdf()
        else:
            return super(Block, self).get_response(request, resource_type, resource_id, args)

    def _create_pdf(self):

        # Dati di esempio
        #order = self.resource.order
        xres = self.resource
        #querySet = self._get_resource_list(self.request).distinct()
        querySet, nSup, nProducts, nPacts = self._get_pdfrecords_pacts(self._get_resource_list(self.request).order_by('name'))
        context_dict = {
            'order' : xres,
            'recSup' : querySet,
            'Suppliers_count' : nSup,
            'pacts_count' : nPacts,
            'products_count' : nProducts,
            'user' : self.request.user,
        }

        REPORT_TEMPLATE = "blocks/%s/report.html" % self.BLOCK_NAME

        template = get_template(REPORT_TEMPLATE)
        context = Context(context_dict)
        html = template.render(context)
        result = StringIO.StringIO()
        #DOMTHU: <th title='TOT account'>&euro;</th>
        #pdf = pisa.pisaDocument(StringIO.StringIO(html), result) 
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1", "ignore")), result)
        #pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8", "ignore")), result ) #, link_callback = fetch_resources )
        if not pdf.err:
            response = HttpResponse(result.getvalue(), mimetype='application/pdf')
            response['Content-Disposition'] = "attachment; filename=Suppliers.pdf"
            return response
        return self.response_error(_('We had some errors<pre>%s</pre>') % cgi.escape(html))


    def fetch_resources(uri, rel):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
        log.debug("Order report Pisa image path (%s)" % path)
        path = os.path.join(settings.MEDIA_ROOT, '/img/icon_beta3.jpg')
        log.debug("Order report Pisa image path (%s)" % path)
        return path


