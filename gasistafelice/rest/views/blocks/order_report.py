from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction, CREATE_PDF, SENDME_PDF, SENDPROD_PDF

from gasistafelice.consts import CREATE, EDIT, EDIT_MULTIPLE, VIEW

from gasistafelice.lib.shortcuts import render_to_xml_response, render_to_context_response

from gasistafelice.supplier.models import Supplier
from gasistafelice.gas.forms.order.gsop import GASSupplierOrderProductForm
from django.forms.formsets import formset_factory

import cgi, os
from django.conf import settings

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

        if request.user == order.gas.tech_referrers \
            or request.user in order.supplier.referrers:

            user_actions += [
                ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE_PDF, verbose_name=_("Create PDF"),
                    popup_form=False,
                ),
            ]

        if request.user == order.referrer_person.user \
            or request.user in order.supplier.referrers:

            if order.is_closed() or order.is_unpaid():
                user_actions += [
                    ResourceBlockAction( 
                        block_name = self.BLOCK_NAME,
                        resource = request.resource,
                        name=SENDME_PDF, verbose_name=_("Send email PDF me"),
                        popup_form=False,
                    ),
                    ResourceBlockAction(
                        block_name = self.BLOCK_NAME,
                        resource = request.resource,
                        name=SENDPROD_PDF, verbose_name=_("Send email PDF producer"),
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

        return formset, records, {}

    def get_response(self, request, resource_type, resource_id, args):

        self.request = request
        self.resource = resource = request.resource

        if args == CREATE_PDF:
            return self._create_pdf()
        if args == SENDME_PDF:
            return self._send_email_logged()
        if args == SENDPROD_PDF:
            return self._send_email_prod()
        else:
            return super(Block, self).get_response(request, resource_type, resource_id, args)

    def _send_email_logged(self):
        try:
            to = self.request.user.email
            self.resource.send_email([to],None, 'Order Email me', self.request.user)
            #FIXME: 'Block' object has no attribute 'response_dict'
            return self.response_success()
        except Exception, e:
            raise self.response_error(_('We had some errors<pre>%s</pre>') % cgi.escape(e.message))

    def _send_email_prod(self):
        try:
            cc = self.request.user.email
            self.resource.send_email_to_supplier([cc], 'Order Email prod', self.request.user)
            return self.response_success()
        except Exception, e:
            raise self.response_error(_('We had some errors<pre>%s</pre>') % cgi.escape(e.message))

    def _create_pdf(self):

        pdf = self.resource.get_pdf_data(requested_by=self.request.user)

        if not pdf.err:
            response = HttpResponse(result.getvalue(), mimetype='application/pdf')
            response['Content-Disposition'] = "attachment; filename=GAS_" + order.get_valid_name() + ".pdf"
            return response
        return self.response_error(_('We had some errors<pre>%s</pre>') % cgi.escape(pdf.err))


    def fetch_resources(uri, rel):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
        log.debug("Order report Pisa image path (%s)" % path)
        path = os.path.join(settings.MEDIA_ROOT, '/img/icon_beta3.jpg')
        log.debug("Order report Pisa image path (%s)" % path)
        return path


