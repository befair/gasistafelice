from django import forms
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from django.core.validators import validate_email
from app_base.validators import validate_phone

from app_base.models import Place, Contact
from app_base.const import STATE_CHOICES, CONTACT_CHOICES
from django.core.exceptions import ValidationError

from app_base.forms.widgets import (
    PlaceWidget, ContactWidget, MultiContactWidget
)

import logging
log = logging.getLogger(__name__)

#--------------------------------------------------------------------------------

class PlaceField(forms.MultiValueField):

    """ Field used to manage a Place model instance.

    DEPRECATED. Now we use ajax_select Field
    """

#    fields = ['address','city']
    widget = PlaceWidget

    def __init__(self, *args, **kw):
        fields = (
            forms.IntegerField(), # was: label=_("id")
            forms.CharField(label=_("name")),
            forms.CharField(label=_("zip")),
            forms.CharField(label=_("city")),
            forms.ChoiceField(label=_("state"),choices=STATE_CHOICES),
        )
        super(PlaceField, self).__init__(fields, *args, **kw)

    def compress(self, data_list):
        if data_list != 0:
            curr_id = data_list[0]
            name = data_list[1]
            zipcode = data_list[2]
            city = data_list[3]
            state = data_list[4]

            if curr_id:
                # get the first object with the same id (should be exactly 1)
                curr_place = Place.objects.get(pk=curr_id)
                curr_place.name = name
                curr_place.zipcode = zipcode
                curr_place.city = city
                curr_place.province = state
            else:
                curr_place = Place(
                    name=name,zipcode=zipcode,
                    city=city,province=state
                )

            curr_place.save()

            return curr_place
        else: 
            return ''

    def clean(self, data_list):
        #log.debug("Clean PlaceField, DL=",data_list)
        nameaddr = data_list[1]
        cap = data_list[2]
        city = data_list[3]
        
        if len(nameaddr) == 0:
            raise ValidationError("A name or address for your place is expected")
        
        if len(city) == 0:
            raise ValidationError("A city is expected")
        
        # trick: save a one space string to make the cap optional - FS
        if len(cap) == 0:
            data_list[2] = " "
        
        
        # strip all input fields
        for i in range(0, len(data_list)-1):
            data_list[i] = data_list[i].strip()
        
        return super(PlaceField, self).clean(data_list)

#--------------------------------------------------------------------------------

class ContactField(forms.MultiValueField):
    """MultiValueField used to manage Contact model instances"""

    widget = ContactWidget

    def __init__(self, *args, **kw):
        fields = (
            forms.IntegerField(),
            forms.ChoiceField(choices=CONTACT_CHOICES,label=_('flavour')),
            forms.CharField(label=_('contact')),
            forms.BooleanField(label=_('preferred'))
        )
        super(ContactField, self).__init__(fields, *args, **kw)
    
    def compress(self, data_list):
        if data_list:
            curr_id = data_list[0]
            flavour = data_list[1]
            contact = data_list[2]
            is_preferred = data_list[3]

            curr_cont = ''
            if curr_id:
                curr_cont = Contact.objects.get(pk=curr_id)
                curr_cont.flavour = flavour
                curr_cont.value = contact
                curr_cont.is_preferred = is_preferred
            else:
                if (contact):
                    curr_cont = Contact(
                        flavour=flavour,value=contact,
                        is_preferred = is_preferred
                    )

            return curr_cont
        return ''
        
    def clean(self, value):
        if value[1].lower() == 'email':
            validate_email(value[2])
        if value[1].lower() == 'phone' and value[2].strip() != "":
            validate_phone(value[2])
        return super(ContactField,self).clean(value)
            
#--------------------------------------------------------------------------------

class MultiContactField(forms.MultiValueField):
    """MultiField to manage "n" ContactField."""

    widget = None

    def __init__(self, n, *args, **kw):
        fields = []

        for i in range(n):
            fields.append(ContactField())

        self.widget = MultiContactWidget(n)

        super(MultiContactField, self).__init__(fields, *args, **kw)

    def set_widget_size(self, n):
        self.widget = MultiContactWidget(n)

    def clean(self, value):
        email_found = False
        for currData in value:
            if currData[1] != None and currData[1].lower() == 'email' and currData[2].strip() != '':
                # at least one email contact -> OK
                email_found = True
                break
                
        if not email_found:
            # no email -> ValidationError
            log.debug("no email found")
            raise forms.ValidationError(_("At least an email contact expected"))
        
        return super(MultiContactField, self).clean(value)

    def compress(self, data_list):
        if self.widget == None:
            return

        # Check if data_list is longer than widget size than possible attack detected!
        if len(data_list) > self.widget.size:
            raise Exception("%d items expected, %d received" %
                (self.widget.size, len(data_list))
            )

        result = []
        email_found = False
 
        # check there is one preferred contact per flavour
        # NB non-specified flavours are ignored
        pref_per_flav = {} # a list of contacts per flavour

        for curr_flav in CONTACT_CHOICES:
            pref_per_flav[curr_flav[0]] = set()

        for curr_contact in data_list:
            if not curr_contact or curr_contact.value.strip() == "":
                continue

            result.append(curr_contact)
            email_found = email_found or (curr_contact.flavour.lower() ==
                "email")

            pref_per_flav[curr_contact.flavour].add(curr_contact)

        for flav,cont_set in pref_per_flav.items():
            if len(cont_set) == 1: # 1 contat for this flavour -> it's preferred
                cont = cont_set.pop()
                cont.is_preferred = True
            elif len(cont_set) > 0:
                found_one_pref = False
                for cont in cont_set:
                    if cont.is_preferred and (not found_one_pref):
                        found_one_pref = True
                    elif cont.is_preferred:
                        raise ValidationError("More than one preferred contact of type %s. Expected only one." % flav)
                
                if not found_one_pref:
                    # no preferred among the contacts -> error
                    raise ValidationError(_("At least one preferred contact of type %s expected.") % flav)


        if email_found == False:
            raise forms.ValidationError("Email contact expected but not found")

        return result
