from django import forms
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from gf.base.models import Place, Contact
from gf.base.const import STATE_CHOICES, CONTACT_CHOICES

#--------------------------------------------------------------------------------

class PlaceWidget(forms.MultiWidget):
    """MultiWidget for place definition.

    DEPRECATED. Because we use ajax_select implementation
    """
    def __init__(self, attrs=None):
        widgets = (
            forms.HiddenInput({ 'value': 0 }),
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs),
            #forms.TextInput(attrs=attrs),
            forms.Select(attrs=attrs, choices=STATE_CHOICES),
        )
        super(PlaceWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            p = Place.objects.get(pk=value)
            return [p.id, p.name, p.zipcode, p.city, p.province]
        else:
            return ['','','','','']

    def format_output(self, rendered_widgets):
        return mark_safe(u'<p class="placewidget">%s %s %s<br />%s %s %s %s %s %s</p>' % (
            _('Name/Address:'), rendered_widgets[1],rendered_widgets[0],
            _('ZIP:'), rendered_widgets[2],
            _('City:'), rendered_widgets[3],
            _('State:'), rendered_widgets[4],
        ))

#--------------------------------------------------------------------------------

class ContactWidget(forms.MultiWidget):
    """MultiWidget used to manage a contact."""

    def __init__(self, attrs={}):
        attrs.update({ 'style' : 'margin-right: 0.5em' })
        widget = (
            forms.HiddenInput(attrs={ 'value':0 }),
            forms.Select(attrs=attrs,choices=CONTACT_CHOICES),
            forms.TextInput(attrs=attrs),
            forms.CheckboxInput(attrs=attrs)
        )
        super(ContactWidget, self).__init__(widget, attrs)

    def decompress(self, value):
        if value:
            c = Contact.objects.get(pk=value)
            return [c.id, c.flavour, c.value,c.is_preferred]
        else:
            return ['','','','']    

    def format_output(self, rendered_widgets):
        return mark_safe(u'<p class="contactwidget">%s %s %s %s %s %s %s</p>' % (
            _('Type')+":", rendered_widgets[1],
            _('Contact')+":", rendered_widgets[2],
            rendered_widgets[0],
            _('Preferred')+":", rendered_widgets[3]
        ))

#--------------------------------------------------------------------------------

class MultiContactWidget(forms.MultiWidget):
    """MultiWidget used to manage "n" contacts."""

    def __init__(self, n, attrs=None):
        widgets = []
        self.num_contacts = n
        for i in range(n):
            widgets.append(ContactWidget())

        super(MultiContactWidget, self).__init__(widgets, attrs)

    @property
    def size(self):
        return self.num_contacts

    def decompress(self, value):
        #log.debug("Compress a MultiContactWidget. Value =", value)
        if value:

            contact_id_set = value
            contacts = []
            for curr_id in contact_id_set:
                if curr_id.isdigit():
                    #log.debug("Search pk=",curr_id)
                    contact_found = Contact.objects.filter(pk=curr_id)
                    #log.debug("Found=",contact_found)
                    if contact_found != None:
                        contacts.append(contact_found)
            
            #log.debug("All contacts=",contacts)
            return contacts
        else:
            return ''

        

