from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers
from django.http import HttpResponse, HttpResponseServerError

from flexi_auth.models import ObjectWithContext

from rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction, CREATE_CSV
from consts import VIEW_CONFIDENTIAL, CONFIDENTIAL_VERBOSE_HTML, CASH
from gf.base.templatetags.accounting_tags import human_readable_account_csv,human_readable_kind, signed_ledger_entry_amount

from django.template.loader import render_to_string

import datetime, csv
import cStringIO as StringIO
#from simple_accounting.models import economic_subject, AccountingDescriptor
#from simple_accounting.models import account_type
#from simple_accounting.exceptions import MalformedTransaction
#from simple_accounting.models import AccountingProxy
#from simple_accounting.utils import register_transaction, register_simple_transaction

#from gf.base.accounting import PersonAccountingProxy

from lib.shortcuts import render_to_xml_response, render_to_context_response

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

#OLD: ENCODING = "iso-8859-1"

class Block(BlockSSDataTables):

    BLOCK_NAME = "transactions"
    BLOCK_DESCRIPTION = _("Economic transactions")
    BLOCK_VALID_RESOURCE_TYPES = ["gas", "supplier", "pact"]

    COLUMN_INDEX_NAME_MAP = {
        0: 'id',
        1: 'transaction__date',
        2: '',
        3: '',
        4: 'amount',
        5: 'transaction__description',
    }

#WAS        2: 'transaction__issuer',
#WAS        3: 'transaction__source',
#WAS        3: 'transaction__kind', --> FIXME: In case of translation the search does not operate correctly

    def __init__(self, *args, **kw):
        
        super(Block, self).__init__(*args, **kw)
        
        # Default start closed. Mainly for GAS -> Accounting tab ("Conto")
        self.start_open   = False

    def _check_permission(self, request):

        if request.resource.gas:
            return request.user.has_perm(
            CASH, obj=ObjectWithContext(request.resource.gas)
            )
        else:
            return True 

    def _get_resource_list(self, request):
        #Accounting.LedgerEntry  or Transactions
        return request.resource.economic_movements

    def get_response(self, request, resource_type, resource_id, args):
        """Check for confidential access permission and call superclass if needed"""

        if not self._check_permission(request): 

            return render_to_xml_response(
                "blocks/table_html_message.xml", 
                { 'msg' : CONFIDENTIAL_VERBOSE_HTML }
            )

        if args == CREATE_CSV:
            return self._create_csv(request)

        return super(Block, self).get_response(request, resource_type, resource_id, args)


#TODO: Filter grid by
# Date From --> To
# Kind iof transctions: can be checkbox list multiselect
# Subject: Radio or multiple checkbox onto values [GAS borselino, GASMemmbers, Suppliers]
#    def options_response(self, request, resource_type, resource_id):
#        """Get options for transaction block.
#        WARNING: call to this method doesn't pass through get_response
#        so you have to reset self.request and self.resource attribute if you want
#        """
#        self.request = request
#        self.resource = request.resource
#        fields = []
#        #DATE FROM
#        fields.append({
#            'field_type'   : 'datetime',
#            'field_label'  : 'from date',
#            'field_name'   : 'from',
#            'field_values' : [{ 'value' : '22/09/2012', 'selected' : ''}]
#        })
#        #DATE TO
#        fields.append({
#            'field_type'   : 'datetime',
#            'field_label'  : 'to date',
#            'field_name'   : 'to',
#            'field_values' : [{ 'value' : '28/09/2012', 'label' : 'labelvalue', 'selected' : 'sel'}]
#        })
#        ctx = {
#            'block_name' : self.description,
#            'fields': fields,
#        }
#        #Can use html template loader
#        return render_to_xml_response('eco-options.xml', ctx)

    def _get_user_actions(self, request):

        user_actions = []

        resource_type = request.resource.resource_type

        if self._check_permission(request):
            user_actions += [
                ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE_CSV, verbose_name=_("Create CSV"),
                    popup_form=False,
                    method="OPENURL",
                ),
            ]

        return user_actions

    def _create_csv(self, request):
        """ Create CSV of this block transactions

            #MATTEO TOREMOVE: lascio la prima implementazione (da levare
            ovviamente dall'integrazione) come monito a me stesso -->
            kiss, kiss e ancora kiss !!

            #NOTA: eliminare nell'integrazione tutte le righe commentate con #OLD:

        """

        headers = [_(u'Id'), _(u'Data'), _(u'Account'), _(u'Kind'), _(u'Cash amount'), _(u'Description')]
        records = self._get_resource_list(request)
        csvfile = StringIO.StringIO()

        writer = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for res in self._get_resource_list(request):
            writer.writerow([res.pk,
                '{0:%a %d %b %Y %H:%M}'.format(res.date),
                human_readable_account_csv(res.account),
                human_readable_kind(res.transaction.kind),
                signed_ledger_entry_amount(res),
                res.transaction.description.encode("utf-8", "ignore")
            ])

        csv_data = csvfile.getvalue()

        if not csv_data:
            rv = HttpResponseServerError(_('Report not generated'))
        else:
            response = HttpResponse(csv_data, content_type='text/csv')
            filename = "%(res)s_%(date)s.csv" % {
                'res': request.resource,
                'date' : '{0:%Y%m%d_%H%M}'.format(datetime.datetime.now())
            }
            response['Content-Disposition'] = "attachment; filename=" + filename
            rv = response
        return rv

