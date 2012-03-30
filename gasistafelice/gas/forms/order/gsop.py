from django import forms
from django.utils.translation import ugettext as _
from django.db import transaction

from gasistafelice.gas.models import GASSupplierOrderProduct 

import logging
log = logging.getLogger(__name__)

#-------------------------------------------------------------------------------

class GASSupplierOrderProductForm(forms.Form):

    id = forms.IntegerField(required=True, widget=forms.HiddenInput)
    enabled = forms.BooleanField(required=False)

    #KO fero: no log here. This code is executed at import time
    #KO fero: log.debug("Create GASSupplierOrderProductForm (%s)" % id)

    #OK fero: this code MUST be under transaction management
    @transaction.commit_on_success
    def save(self):

        id = self.cleaned_data.get('id')
        # log.debug("Save GASSupplierOrderProductForm id(%s)" % id)

        if id:
            enabled = self.cleaned_data.get('enabled')
            # log.debug("Save GASSupplierOrderProductForm enabled(%s)" % enabled)
            # Delete is ok for gsop that have gmo but: 
            # FIXME: if no gmo associated to gsop the field enabled remain always True?
            if not enabled:
                gsop = GASSupplierOrderProduct.objects.get(pk=id)
                log.debug("Making UNAVAILABLE orderable product %s in order %s" % (gsop, gsop.order.pk))
                log.debug(u"GASSupplierOrderProductForm status: [amount=euro %s, gasmembers=%s]" % (
                    gsop.tot_amount, gsop.tot_gasmembers
                ))
                gsop.delete()


class GASSupplierOrderProductInterGAS(forms.Form):

    id = forms.IntegerField(required=True, widget=forms.HiddenInput)
    enabled = forms.BooleanField(required=False)

    @transaction.commit_on_success
    def save(self):

        id = self.cleaned_data.get('id')
        # log.debug("Save GASSupplierOrderProductInterGAS id(%s)" % id)

        if id:
            enabled = self.cleaned_data.get('enabled')
            # log.debug("Save GASSupplierOrderProductForm enabled(%s)" % enabled)
            # Delete is ok for gsop that have gmo but: 
            # FIXME: if no gmo associated to gsop the field enabled remain always True?
            if not enabled:
                gsop = GASSupplierOrderProduct.objects.get(pk=id)
                log.debug("Making UNAVAILABLE orderable product %s in order %s" % (gsop, gsop.order.pk))
                log.debug(u"GASSupplierOrderProductInterGAS status: [amount=euro %s, gasmembers=%s]" % (
                    gsop.tot_amount, gsop.tot_gasmembers
                ))
                gsop.delete()

