from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from gasistafelice.gas.models import GAS, GASMember, GASMemberOrder, GASSupplierOrder
from gasistafelice.supplier.models import Supplier

from django.forms.formsets import formset_factory
from django.forms import widgets
from django.contrib.admin import widgets as admin_widgets

from gasistafelice.lib.formsets import BaseFormSetWithRequest

from flexi_auth.models import ParamRole, PrincipalParamRoleRelation
from gasistafelice.consts import GAS_REFERRER_CASH, GAS_REFERRER_SUPPLIER

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

    log.debug("    --------------       EcoGASMemberForm")
    purchaser_id = forms.IntegerField(required=False)
    ord_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    gm_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    eco_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    amounted = forms.DecimalField(required=False, initial=0) #, widget=forms.TextInput())
    #note = forms.CharField(required=False, widget=forms.TextInput(), max_length=64)

    def __init__(self, request, *args, **kw):
        super(EcoGASMemberForm, self).__init__(*args, **kw)
        self.fields['amounted'].widget.attrs['class'] = 'taright'
        self.fields['purchaser_id'].widget.attrs['readonly'] = True
        self.fields['purchaser_id'].widget.attrs['disabled'] = 'disabled'
        self.fields['purchaser_id'].widget.attrs['class'] = 'input_small'
        self.__loggedusr = request.user

    def save(self):

        #Control logged user
        if not self.__loggedusr:
            raise forms.ValidationError(_('cannot identify the logged in user. Please try loggin. Cannot continue'))
            log.debug("EcoGASMemberForm cannot identify the logged in user.")
            return

        _gm_id = self.cleaned_data.get('gm_id')
        _ord_id = self.cleaned_data.get('ord_id')
        _eco_id = self.cleaned_data.get('eco_id')
        #FIXME DEBUG EcoGASMemberForm identifiers [None/None]
        log.debug("EcoGASMemberForm identifiers [%s/%s]", _ord_id, _gm_id )
        print "EcoGASMemberForm identifiers [%s/%s]" % (_ord_id, _gm_id)
        if not _gm_id or not _ord_id:
            raise forms.ValidationError(_('cannot retrieve GASMember and Order identifiers. Cannot continue'))
            log.debug("EcoGASMemberForm cannot retrieve GASMember and Order identifiers")
            return
        order = GASSupplierOrder.objects.get(pk=_ord_id)
        gm = GASMember.objects.get(pk=_gm_id)
        if not gm or not order:
            raise forms.ValidationError(_('cannot retrieve GASMember and Order datas. Cannot continue'))
            log.debug("EcoGASMemberForm cannot retrieve GASMember and Order datas. Identifiers (%s/%s)." % (_ord_id,_gm_id))
            return
        #TODO: Seldon or Fero. Control if Order is in the rigth Workflow STATE

        #TODO: Control is CASH REFERRER for this GAS
        if self.__loggedusr not in order.pact.gas.cash_referrers:
            log.warn("!!!!EcoGASMemberForm (%s) Not authorized %s. Identifiers (%s/%s)" % (self.__loggedusr,gm,_ord_id,_gm_id))
            raise forms.ValidationError(_('Not authorized'))
            return

        #Do economic work
        #TODO: gas.accounting.withdraw_from_member_account(self, member, amount, refs=None):
        amounted = self.cleaned_data.get('amounted')
        try:
            if amounted == 0:
                #Find existing movment and delete it
                log.error("ECO Order GasMember(%s) - Delete? - (%s) " % (gm, amounted))
            else:
                #Find existing movment
                #If exist UPDATE
                #    log.warn("ECO Order GasMember(%s) - Update - (%s) " % (gm, amounted))
                #Else CREATE Movement between GASMember.account --> GAS.account
                log.warn("ECO Order GasMember(%s) - Create - (%s) " % (gm, amounted))
        except:
            log.error("ERR: EcoGASMemberForm (%s) Not authorized %s. Identifiers (%s/%s) Euro: %s." % (self.__loggedusr,gm,_ord_id,_gm_id, amounted))
            raise forms.ValidationError(_('ERR: EcoGASMemberForm. Context not satisfied'))

