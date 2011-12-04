from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from gasistafelice.gas.models import GAS, GASMember, GASMemberOrder, GASSupplierOrder
from gasistafelice.supplier.models import Supplier

from django.forms.formsets import formset_factory
from django.forms import widgets
from django.contrib.admin import widgets as admin_widgets

from gasistafelice.lib.formsets import BaseFormSetWithRequest
from gasistafelice.lib.fields.forms import CurrencyField

from flexi_auth.models import ParamRole, PrincipalParamRoleRelation
from flexi_auth.models import ObjectWithContext
from gasistafelice.consts import CASH

from datetime import datetime
import logging
log = logging.getLogger(__name__)

from django.core import validators
from django.core.exceptions import ValidationError


#-------------------------------------------------------------------------------


class EcoGASMemberForm(forms.Form):
    """Return form class for row level operation on cash ordered data
    use in Curtail
    Movement between GASMember.account --> GAS.account
    """

    gm_id = forms.IntegerField(widget=forms.HiddenInput)
    entry_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    amounted = CurrencyField(required=False, initial=0) #, widget=forms.TextInput())

    #TODO: domthu: note and delete
    #note = forms.CharField(required=False, widget=forms.TextInput(), max_length=64)

    def __init__(self, request, *args, **kw):
        log.debug("    --------------       EcoGASMemberForm")
        super(EcoGASMemberForm, self).__init__(*args, **kw)
        self.fields['amounted'].widget.attrs['class'] = 'taright'
        self.__loggedusr = request.user
        self.__order = request.resource.order

    def clean(self):

        cleaned_data = super(EcoGASMemberForm, self).clean()
        print("cleaned_data %s" % cleaned_data)
        try:
            cleaned_data['gasmember'] = GASMember.objects.get(pk=cleaned_data['gm_id'])
        except KeyError:
            log.debug("EcoGASMemberForm: cannot retrieve GASMember identifier. FORM ATTACK!")
            raise 
        except GASMember.DoesNotExist:
            log.debug("EcoGASMemberForm: cannot retrieve GASMember instance. Identifier (%s)." % cleaned_data['gm_id'])
            raise
           
        try:
            cleaned_data['entry'] = LedgerEntry.objects.get(pk=cleaned_data['entry_id'])
        except LedgerEntry.DoesNotExist:
            log.debug("EcoGASMemberForm: ledger entry not found for order %s and gasmember %s" % (
                self.__order.pk, cleaned_data['gasmember'].pk)
            )
            cleaned_data['entry'] = None

        return cleaned_data

    def save(self):

        #Control logged user
        #if self.__loggedusr not in self.__order.cash_referrers: KO if superuser
        if not self.__loggedusr.has_perm(CASH, 
            obj=ObjectWithContext(self.__order.gas)
        ):

            log.debug("PermissionDenied %s in cash order form" % self.__loggedusr)
            raise PermissionDenied("You are not a cash_referrer, you cannot update GASMembers cash!")

        gm = self.cleaned_data['gasmember']
        entry = self.cleaned_data['entry']

        #TODO: Seldon or Fero. Control if Order is in the rigth Workflow STATE

        #Do economic work
        amounted = self.cleaned_data.get('amounted')

        if amounted:
            # This kind of amount is ever POSITIVE!
            amounted = abs(amounted)

            refs = [gm, self.__order]

            if entry:
                # A ledger entry already exists
                if entry.amount != amounted:
                    gm.gas.accounting.withdraw_from_member_account_update(
                        gm, amounted, refs
                    )

            else:
                gm.gas.accounting.withdraw_from_member_account(gm, amounted, refs)

