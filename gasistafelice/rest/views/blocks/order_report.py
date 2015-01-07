from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import ( BlockSSDataTables, ResourceBlockAction, 
    CREATE_PDF, CREATE_HTML, SENDME_PDF, SENDPROD_PDF,
    VIEW_AS_HTML
)

from gasistafelice.consts import CREATE, EDIT, EDIT_MULTIPLE, VIEW

from gasistafelice.lib.shortcuts import render_to_xml_response, render_to_context_response

from gasistafelice.supplier.models import Supplier
from gasistafelice.base.models import Person
from gasistafelice.gas.forms.order.gsop import GASSupplierOrderProductForm
from django.forms.formsets import formset_factory

import cgi, os
from django.http import HttpResponse

from flexi_auth.models import ObjectWithContext

import logging
log = logging.getLogger(__name__)

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "order_report"
    BLOCK_DESCRIPTION = _("Order report")
    BLOCK_VALID_RESOURCE_TYPES = ["order"] 

    COLUMN_INDEX_NAME_MAP = {
        0: 'pk', 
        1: 'gasstock__stock__product',
        2: 'order_price',
        3: 'has_changed',
        4: 'tot_gasmembers',
        5: 'unconfirmed_orders',
        6: 'tot_amount',
        7: 'tot_price',
        8: 'enabled'
    }

    def _get_user_actions(self, request):
  
        user_actions = []

        order = self.resource.order

        #TODO fero: add permission GET_ORDER_DOC
        if request.user == order.gas.tech_referrers \
            or request.user in order.gas.supplier_referrers \
            or request.user in order.supplier.referrers \
            or request.user.is_superuser:

            user_actions += [
                ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE_PDF, verbose_name=_("Create PDF"),
                    popup_form=False,
                    method="OPENURL",
                ),
            ]
            
            user_actions += [
                ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name="createhtml", verbose_name=_("Create HTML"),
                    popup_form=False,
                ),
            ]

#            user_actions += [
#                ResourceBlockAction(
#                    block_name = self.BLOCK_NAME,
#                    resource = request.resource,
#                    name=VIEW_AS_HTML, verbose_name=_("Visualizza come HTML"),
#                    popup_form=True,
#                ),
#            ]

        #TODO fero: permission GET_ORDER_DOC
        if request.user == order.referrer_person.user \
            or request.user in order.gas.supplier_referrers \
            or request.user in order.supplier.referrers \
            or request.user.is_superuser:

            if order.is_closed() or order.is_unpaid():
                user_actions += [
                    ResourceBlockAction( 
                        block_name = self.BLOCK_NAME,
                        resource = request.resource,
                        name=SENDME_PDF, verbose_name=_("Send email PDF me"),
                        popup_form=False,
                    )
                ]
                if order.supplier.config.receive_order_via_email_on_finalize:                        
                    user_actions += [
                        ResourceBlockAction(
                            block_name = self.BLOCK_NAME,
                            resource = request.resource,
                            name=SENDPROD_PDF, verbose_name=_("Send email PDF supplier"),
                            popup_form=False,
                        )
                    ]



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
        #return request.resource.stocks
        # GASSupplierOrderProduct objects
        return request.resource.orderable_products.filter(
            gasmember_order_set__ordered_amount__gt=0
        ).distinct()

    def _get_resource_families(self, request):
        return request.resource.ordered_products

    def _get_edit_multiple_form_class(self):
        qs = self._get_resource_list(self.request)
        return formset_factory(
            form=GASSupplierOrderProductForm,
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

        formset = self._get_edit_multiple_form_class()(data)

        records = []
        for i, el in enumerate(querySet):

            form = formset[map_info[el.pk]['formset_index']]

            records.append({
               'id' : el.pk,
               'product' : el.product,
               'price' : el.order_price,
               'price_changed' : el.has_changed_price,
               'tot_gasmembers' : el.tot_gasmembers,
               'unconfirmed' : el.unconfirmed_orders,
               'ordered_amount' : el.tot_amount,
               'ordered_total' : el.tot_price,
               'field_enabled' : "%s %s" % (form['id'], form['enabled']),
            })
               #'gasstock' : el.gasstock,

        return formset, records, {}

    def get_response(self, request, resource_type, resource_id, args):

        try:
            rv = super(Block, self).get_response(request, resource_type, resource_id, args)
        except NotImplementedError:
            # Not implemented args are implemented in this method
            pass

        if args == CREATE_PDF:
            rv = self._create_pdf()
        elif args == VIEW_AS_HTML:
            rv = self._render_as_html()
        elif args == SENDME_PDF:
            rv = self._send_email_logged()
        elif args == SENDPROD_PDF:
            rv = self._send_email_supplier()
        #MOD
        elif args == CREATE_HTML:
            rv = self._create_html()
        
#        #TODO FIXME: ugly patch to fix AFTERrecords.append( 6
#        if args == self.KW_DATA:
#            from gasistafelice.lib.views_support import prepare_datatables_queryset, render_datatables
#            
#            querySet = self._get_resource_list(request) 
#            #columnIndexNameMap is required for correct sorting behavior
#            columnIndexNameMap = self.COLUMN_INDEX_NAME_MAP
#            #path to template used to generate json (optional)
#            jsonTemplatePath = 'blocks/%s/data.json' % self.BLOCK_NAME

#            val_querySet, dt_params = prepare_datatables_queryset(request, querySet, columnIndexNameMap)
#            #TODO FIXME: AFTER 6 
#            formset, records, moreData = self._get_records(request, querySet)
#            rv = render_datatables(request, records, dt_params, jsonTemplatePath)

        return rv

    def _send_email_logged(self):
        try:
            to = Person.objects.get(user=self.request.user).preferred_email_address
            self.resource.send_email([to],None, 'Order Email me', self.request.user)
            return self.response_success()
        except Exception, e: 
            raise
            #exceptions must be old-style classes or derived from BaseException, not HttpResponse
            raise self.response_error(_('We had some errors<pre>%s</pre>') % cgi.escape(e.message))

    def _send_email_supplier(self):
        try:
            cc = Person.objects.get(user=self.request.user).preferred_email_address
            self.resource.send_email_to_supplier([cc], 'Order Email prod', self.request.user)
            return self.response_success()
        except Exception, e:
            raise self.response_error(_('We had some errors<pre>%s</pre>') % cgi.escape(e.message))

    def _create_pdf(self):

        pdf_data = self.resource.get_pdf_data(requested_by=self.request.user)

        if not pdf_data:
            rv = self.response_error(_('Report not generated')) 
        else:
            response = HttpResponse(pdf_data, mimetype='application/pdf')
            response['Content-Disposition'] = "attachment; filename=" + self.resource.get_valid_name() + ".pdf" 
            rv = response
        return rv
    #MOD
    def _create_html(self):
        
        html_data = self.resource.get_html_data(requested_by=self.request.user)

        if not html_data:
            rv = self.response_error(_('Report not generated')) 
        else:
            response = HttpResponse(html_data, mimetype='text/html')
            response['Content-Disposition'] = "attachment; filename=" + self.resource.get_valid_name() + ".html" 
            rv = response
        return rv

    def _render_as_html(self):

        html = self.resource.render_as_html(requested_by=self.request.user)
        return HttpResponse(html)

    def fetch_resources(uri, rel):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
        log.debug("Order report Pisa image path (%s)" % path)
        path = os.path.join(settings.MEDIA_ROOT, '/img/icon_beta3.jpg')
        log.debug("Order report Pisa image path (%s)" % path)
        return path


