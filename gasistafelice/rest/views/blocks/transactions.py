from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers
from django.http import HttpResponse

from flexi_auth.models import ObjectWithContext

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction, CREATE_CSV
from gasistafelice.consts import VIEW_CONFIDENTIAL, CONFIDENTIAL_VERBOSE_HTML, CASH

#OLD: from gasistafelice.lib import get_params_from_template
#OLD: from gasistafelice.lib.csvmanager import CSVManager

#OLD: from gasistafelice.base.models import Person
#OLD: from gasistafelice.gas.models.base import GAS
#OLD: from gasistafelice.supplier.models import Supplier

from django.template.loader import render_to_string

import datetime

#from simple_accounting.models import economic_subject, AccountingDescriptor
#from simple_accounting.models import account_type
#from simple_accounting.exceptions import MalformedTransaction
#from simple_accounting.models import AccountingProxy
#from simple_accounting.utils import register_transaction, register_simple_transaction

#from gasistafelice.base.accounting import PersonAccountingProxy

from gasistafelice.lib.shortcuts import render_to_xml_response, render_to_context_response

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


    def _get_resource_list(self, request):
        #Accounting.LedgerEntry  or Transactions
        return request.resource.economic_movements

    def get_response(self, request, resource_type, resource_id, args):
        """Check for confidential access permission and call superclass if needed"""

        if request.resource.gas and not request.user.has_perm(
            CASH, obj=ObjectWithContext(request.resource.gas)
        ): 

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

        if request.resource.gas and not request.user.has_perm(
            CASH, obj=ObjectWithContext(request.resource.gas)
        ):

            return user_actions

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

        #OLD: template = "%(Id)s %(Data)s %(Conto)s %(Kind)s %(Cash amount)s %(Descrizione)s"
        #OLD: delimiter = ';'
        #OLD: fieldnames = get_params_from_template(template)
        #OLD: data = []
        records = self._get_resource_list(request)

        #OLD: reference to rest/templates/blocks/transactions/data.json
        #OLD: for res in self._get_resource_list(request):
        #OLD:    data.append(
        #OLD:        {'Id' : res.pk,
        #OLD:         'Data' : '{0:%a %d %b %Y %H:%M}'.format(res.date),
        #OLD:         'Conto' : self.human_readable_account(res.account),
        #OLD:         'Kind' : res.transaction.kind,
        #OLD:         'Cash amount' : res.amount,
        #OLD:         'Descrizione' : res.transaction.description.encode("utf-8", "ignore")
        #OLD:        }
        #OLD:    )

        csv_data = render_to_string('blocks/transactions/data.csv', { 'records' : records })
        #OLD: manager = CSVManager(fieldnames=fieldnames, delimiter=delimiter, encoding=ENCODING)
        #OLD: csv_data = manager.write(data)

        if not csv_data:
            rv = self.response_error(_('Report not generated'))
        else:
            response = HttpResponse(csv_data, mimetype='text/csv')
            filename = "%(res)s_%(date)s.csv" % {
                'res': request.resource,
                'date' : '{0:%Y%m%d_%H%M}'.format(datetime.datetime.now())
            }
            response['Content-Disposition'] = "attachment; filename=" + filename
            rv = response
        return rv

    #OLD: def human_readable_account(self,account):
    #OLD:     """
    #OLD:         Return one string containing the resource
    #OLD:     """
    #OLD:     name = ""
    #OLD:     if 'person-' in account.name:
    #OLD:         p_pk = account.name.replace("person-", "")
    #OLD:         try:
    #OLD:             obj = Person.objects.get(pk=p_pk)
    #OLD:         except GASMember.DoesNotExist:
    #OLD:             pass
    #OLD:         else:
    #OLD:             name = obj.report_name

    #OLD:     elif 'gas-' in account.name:
    #OLD:         p_pk = account.name.replace("gas-", "")
    #OLD:         try:
    #OLD:             obj = GAS.objects.get(pk=p_pk)
    #OLD:         except GAS.DoesNotExist:
    #OLD:             pass
    #OLD:         else:
    #OLD:             name = obj.id_in_des

    #OLD:     elif 'supplier-' in account.name:
    #OLD:         p_pk = account.name.replace("supplier-", "")
    #OLD:         try:
    #OLD:             obj = Supplier.objects.get(pk=p_pk)
    #OLD:         except Supplier.DoesNotExist:
    #OLD:             pass
    #OLD:         else:
    #OLD:             name = obj.name

    #OLD:     if name == "":
    #OLD:         name = "%s" % account.system.owner.instance

    #OLD:     return "%(name)s " % {'name': name.encode("utf-8", "ignore")}
