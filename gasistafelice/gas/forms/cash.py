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


#-------------------------------------------------------------------------------


class EcoGASMemberForm(forms.Form):
    """Return form class for row level operation on cash ordered data
    use in Curtail
    Movement between GASMember.account --> GAS.account
    """

    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    log.debug("EcoGASMemberForm (%s)" % id)
    gm_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    amounted = forms.DecimalField(required=False, initial=0) #, widget=forms.TextInput())
    #note = forms.CharField(required=False, widget=forms.TextInput(), max_length=64)

    def __init__(self, request, *args, **kw):
        super(EcoGASMemberForm, self).__init__(*args, **kw)
        self.fields['amounted'].widget.attrs['class'] = 'taright'
        self.__loggedusr = request.user

    def save(self):

        #Control is CASH REFERRER
        if not self.__loggedusr or self.__gmusr != self.__loggedusr:
            log.debug("------SingleGASMemberOrderForm (%s) not enabled for %s" % (self.__gmusr,self.__loggedusr))
            return
        id = self.cleaned_data.get('id')
        amounted = self.cleaned_data.get('amounted')
        if id:
            gm = GASMember.objects.get(pk=id)
            amounted = self.cleaned_data.get('amounted')
            if amounted == 0:
                #Find existing movment and delete it
                log.error("ECO Order GasMember(%s) - Delete? - (%s) " % (gm, amounted))
            else:
                #Find existing movment 
                #If exist UPDATE
                #    log.warn("ECO Order GasMember(%s) - Update - (%s) " % (gm, amounted))
                #Else CREATE Movement between GASMember.account --> GAS.account
                log.warn("ECO Order GasMember(%s) - Create - (%s) " % (gm, amounted))

        else:
            log.warn("ECO Order GasMember(%s) - ?? - (%s) " % (self.__loggedusr, amounted))


