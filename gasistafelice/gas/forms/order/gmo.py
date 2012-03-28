from django.db import transaction
from django import forms
from django.utils.translation import ugettext as _

from gasistafelice.gas.models import GASMemberOrder, GASSupplierOrderProduct
from gasistafelice.exceptions import DatabaseInconsistent

import logging
log = logging.getLogger(__name__)

#-------------------------------------------------------------------------------

class BaseGASMemberOrderForm(forms.Form):
    """Base class for GASMemberOrder row level operations.

    Do not use this class in your views, use subclasses instead."""

    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    gsop_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    ordered_amount = forms.DecimalField(required=False, initial=0)
    ordered_price = forms.DecimalField(required=False, widget=forms.HiddenInput)

    #KO fero: no log here. This code is executed at import time
    #KO fero: log.debug("Create BaseGASMemberOrderForm (%s)" % id)

    def __init__(self, request, *args, **kw):

        super(BaseGASMemberOrderForm, self).__init__(*args, **kw)
        self._gm = request.resource.gasmember
        self._gmusr = request.resource.gasmember.person.user
        self._loggedusr = request.user

    def clean(self):
        cleaned_data = super(BaseGASMemberOrderForm, self).clean()

        #COMMENT LF: specifications say that every GASMember MUST
        #COMMENT LF: be bound to a User: so raise an Exception if not True
        if not self._gmusr:
            raise DatabaseInconsistent(
                "Member %s is not bound to a valid User" % self._gm
            )

        if self._gmusr != self._loggedusr:
            #DELEGATE: order.referrer_person can make order in name of other person
            #In this case we can authorize and set in the note the person who act the gasmemberorder
            id = self.cleaned_data.get('id')
            if id:
                gmo = GASMemberOrder.objects.get(pk=id)
                if gmo.ordered_amount != self.cleaned_data.get('ordered_amount'): 
                    #if not self._loggedusr == gmo.order.referrer_person.user:
                    if not gmo.can_delegate(self._loggedusr):

                        log.debug(u"---- %s (%s) BASE VALIDATION not enabled for %s" % (
                            self.__class__.__name__,
                            self._gmusr, self._loggedusr
                        ))
                        raise forms.ValidationError(
                            _(u"You %(logged)s are not authorized to make an order for %(person)s") % {
                                'logged' : u"(%s)" % self._loggedusr, 
                                'person' :self._gmusr
                        })
        return cleaned_data



#-------------------------------------------------------------------------------

class SingleGASMemberOrderForm(BaseGASMemberOrderForm):
    """Return form class for row level operation on GSOP datatable"""

    note = forms.CharField(required=False, widget=forms.TextInput(), max_length=64)

    def __init__(self, *args, **kw):
        super(SingleGASMemberOrderForm, self).__init__(*args, **kw)
        self.fields['note'].widget.attrs['class'] = 'input_medium'

    @transaction.commit_on_success
    def save(self):

        if self.is_valid():
            id = self.cleaned_data.get('id')
            if id:
                gmo = GASMemberOrder.objects.get(pk=id)
                gmo.ordered_price = self.cleaned_data.get('ordered_price')
                gmo.ordered_amount = self.cleaned_data.get('ordered_amount')
                gmo.note = self.cleaned_data.get('note')

                if self._gmusr != self._loggedusr:
                    #if self._loggedusr == gmo.order.referrer_person.user:
                    if gmo.can_delegate(self._loggedusr):
                        log.debug(u"---- %s (%s) DELEGATE UPDATE for %s" % (
                            self.__class__.__name__,
                            self._gmusr, self._loggedusr
                        ))
                        delegate = _("[ord by %s] ") % gmo.order.referrer_person.report_name
                        if gmo.note.find(delegate) == -1:
                            gmo.note = delegate + gmo.note
                    else:
                        log.debug(u"---- %s (%s) DELEGATE UPDATE not enabled for %s" % (
                            self.__class__.__name__,
                            self._gmusr, self._loggedusr
                        ))
                        raise forms.ValidationError(
                            _(u"You %(logged)s are not authorized to update an order for %(person)s") % {
                                'logged' : u"(%s)" % self._loggedusr, 
                                'person' :self._gmusr
                        })
                        return;

                if gmo.ordered_amount == 0:
                    log.debug(u"REMOVING GASMemberOrder (%s) from amount widget (+ -)" % gmo.pk)
                    gmo.delete()
                    log.debug("REMOVED")
                else:
                    log.debug(u"UPDATING GASMemberOrder (%s) " % gmo.pk)
                    gmo.save()
                    log.debug("UPDATED")

            elif self.cleaned_data.get('ordered_amount'):
                    gsop = GASSupplierOrderProduct.objects.get(pk=self.cleaned_data.get('gsop_id'))
                    note = self.cleaned_data.get('note')
                    #if self._gmusr != self._loggedusr and self._loggedusr == gsop.order.referrer_person.user:
                    if self._gmusr != self._loggedusr:
                        if gsop.can_delegate(self._loggedusr):
                            log.debug(u"---- %s (%s) DELEGATE CREATE for %s" % (
                                self.__class__.__name__,
                                self._gmusr, self._loggedusr
                            ))
                            #delegate = _("[ord by %s] ") % gsop.order.referrer_person.report_name
                            delegate = _("[ord by %s] ") % self._loggedusr
                            if note.find(delegate) == -1:
                                note = delegate + note
                        else:
                            log.debug(u"---- %s (%s) DELEGATE CREATE not enabled for %s" % (
                                self.__class__.__name__,
                                self._gmusr, self._loggedusr
                            ))
                            raise forms.ValidationError(
                                _(u"You %(logged)s are not authorized to create an order for %(person)s") % {
                                    'logged' : u"(%s)" % self._loggedusr, 
                                    'person' :self._gmusr
                            })
                            return;

                    # INTEGRITY NOTE: Ensure no duplicate entry into database is done 
                    # into GASMemberOrder Model with set unique_together
                    gmo = GASMemberOrder(
                            ordered_product = gsop,
                            ordered_price = self.cleaned_data.get('ordered_price'),
                            ordered_amount = self.cleaned_data.get('ordered_amount'),
                            note = note,
                            purchaser = self._gm,
                    )
                    gmo.save()
                    log.debug("CREATED GASMemberOrder (%s) " % gmo.pk)
        else:
            log.warning("SingleGASMemberOrderForm.save(): form is not valid. is_valid() SHOULD be called before calling save()")

#-------------------------------------------------------------------------------

class BasketGASMemberOrderForm(BaseGASMemberOrderForm):
    """Return form class for row level operation on GMO datatable"""

    gm_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    enabled = forms.BooleanField(required=False)

    @transaction.commit_on_success
    def save(self):

        # COMMENT fero: removed some checks that are done in .clean()
        # which is always called in form.is_valid()
        # that we MUST perform always when dealing with forms
        # (maybe we can include a call to it in this method...)

        if self.is_valid():

            id = self.cleaned_data.get('id')
            gm_id = self.cleaned_data.get('gm_id')
            gsop_id = self.cleaned_data.get('gsop_id')
            enabled = self.cleaned_data.get('enabled')

            if id:
                gmo = GASMemberOrder.objects.get(pk=id)
    #            if gm_id and gm_id != gmo.purchaser.pk:
    #                print "Qualcosa non va con: GASmember"
    #                return ""
                #On basket do nothing if no change needed
                if gmo.ordered_amount != self.cleaned_data.get('ordered_amount') or enabled: 

                    if self._gmusr != self._loggedusr:
                        #if self._loggedusr == gmo.order.referrer_person.user:
                        if gmo.can_delegate(self._loggedusr):
                            #delegate = _("[ord by %s] ") % gmo.order.referrer_person.report_name
                            delegate = _("[ord by %s] ") % self._loggedusr
                            if gmo.note.find(delegate) == -1:
                                gmo.note = delegate + gmo.note
                            log.debug(u"---- %s (%s) DELEGATE BASKET for %s" % (
                                self.__class__.__name__,
                                self._gmusr, self._loggedusr
                            ))
                        else:
                            log.debug(u"---- %s (%s) DELEGATE BASKET not enabled for %s" % (
                                self.__class__.__name__,
                                self._gmusr, self._loggedusr
                            ))
                            raise forms.ValidationError(
                                _(u"You %(logged)s are not authorized to modify order's basket for %(person)s") % {
                                    'logged' : u"(%s)" % self._loggedusr, 
                                    'person' :self._gmusr
                            })
                            return;
                
                    gmo.ordered_price = self.cleaned_data.get('ordered_price')
                    gmo.ordered_amount = self.cleaned_data.get('ordered_amount')
                    # log.debug("BasketGASMemberOrderForm (%s) enabled = %s" % (gmo.pk,enabled))
                    if gmo.ordered_amount == 0:
                        log.debug(u"REMOVING GASMemberOrder (%s) from BASKET using amount widget (+ -)")
                        gmo.delete()
                        log.debug(u"REMOVED")
                    elif enabled:
                        log.debug(u"REMOVING GASMemberOrder (%s) from BASKET using check enabled")
                        gmo.delete()
                        log.debug(u"REMOVED")
                    else:
                        log.debug(u"UPDATING GASMemberOrder (%s) from BASKET" % id)
                        gmo.save()
                        log.debug(u"UPDATED")
                #else:
                #    log.debug(u"NOTHING TODO NOTHING")
        else:
            log.warning("BasketGASMemberOrderForm.save(): form is not valid. is_valid() SHOULD be called before calling save()")


