from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from gasistafelice.gas.models import GAS, GASMember, GASMemberOrder, GASSupplierOrder
from gasistafelice.supplier.models import Supplier

from django.forms.formsets import formset_factory
from django.forms import widgets
from django.contrib.admin import widgets as admin_widgets

from gasistafelice.lib.formsets import BaseFormSetWithRequest

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

    log.debug("    --------------       EcoGASMemberForm")
    purchaser_id = forms.IntegerField(required=False)
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
        self.__order = request.resource.order

    def save(self):

        #Control logged user
        #if self.__loggedusr not in self.__order.cash_referrers: KO if superuser
        if not self.__loggedusr.has_perm(CASH, 
            obj=ObjectWithContext(self.__order.gas)
        ):

            log.debug("PermissionDenied %s in cash order form" % self.__loggedusr)
            raise PermissionDenied("You are not a cash_referrer, you cannot update GASMembers cash!")

        _gm_id = self.cleaned_data.get('gm_id')
        _eco_id = self.cleaned_data.get('eco_id')
        #FIXME DEBUG EcoGASMemberForm identifiers [None/None]
        log.debug("EcoGASMemberForm identifiers [%s/%s]" % (self.__order.pk, _gm_id ))
        print "EcoGASMemberForm identifiers [%s/%s]" % (self.__order.pk, _gm_id)
        if not _gm_id:
            log.debug("EcoGASMemberForm cannot retrieve GASMember and Order identifiers")
            raise forms.ValidationError(_('cannot retrieve GASMember and Order identifiers. Cannot continue'))

        try:
            gm = GASMember.objects.get(pk=_gm_id)
        except GASMember.DoesNotExist:
            log.debug("EcoGASMemberForm cannot retrieve GASMember and Order datas. Identifiers (%s)." % _gm_id)
            raise forms.ValidationError(_('cannot retrieve GASMember and Order datas. Cannot continue'))

        #TODO: Seldon or Fero. Control if Order is in the rigth Workflow STATE

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

