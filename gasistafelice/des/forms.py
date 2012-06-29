# -*- coding: utf-8 -*-

from registration.forms import RegistrationFormUniqueEmail
from django import forms
from django.db import transaction
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from captcha.fields import CaptchaField

from flexi_auth.models import ParamRole, PrincipalParamRoleRelation
from gasistafelice.consts import SUPPLIER_REFERRER, GAS_MEMBER

from gasistafelice.gas.models import GAS, GASMember
from gasistafelice.supplier.models import Supplier
from gasistafelice.base.models import Place, Contact, Person

from registration.models import RegistrationProfile

import logging
log = logging.getLogger(__name__)

class DESRegistrationForm(RegistrationFormUniqueEmail):

    gas_choice = forms.ModelChoiceField(
        label="Sei del gas...",
        queryset = GAS.objects.all(),
        required=False,
        help_text=_("after your registration you have to wait for account activation by a GAS tech referrer")
    )
    supplier_choice = forms.ModelChoiceField(
        label="Sei il fornitore...",
        queryset = Supplier.objects.all(),
        required=False,
        help_text=_("if you are not in this list, or you are the first user for this supplier, please contact a GAS tech referrer that could activate your account.")
    )

    name = forms.CharField( label="Nome")
    surname = forms.CharField( label="Cognome")
    city = forms.CharField(label="Città")
    phone = forms.CharField(
        label="Numero di telefono",
        required=True,
        help_text="È importante poter contattare chi si registra via telefono"
    )
    motivation = forms.CharField(label='Motivazione', required=False, widget=forms.Textarea,
        help_text="Alcune righe per conoscerti e/o sapere come ai conosciuto il GAS")
    recaptcha = CaptchaField(label="Inserisci le lettere che leggi " + 
        "per farci capire che non sei un programma automatico"
    )

    def clean(self):
        cleaned_data = super(DESRegistrationForm, self).clean()
        if not ( 
            self.cleaned_data.get('gas_choice') or
            self.cleaned_data.get('supplier_choice')
        ):
            raise forms.ValidationError("Devi registrarti in un GAS o in un fornitore esistente")

        return cleaned_data

    @transaction.commit_on_success
    def save(self):
        """Start the registration process after a new user completed the registration form.

        WAS: Steps:
        WAS: 1. create User
        WAS: 2. bind User to appropriate role in Supplier and/or GAS
        WAS: 3. Send email to GAS_REFERRER_TECH or all GAS_REFERRER_TECHs if the new user is bound to Supplier
        WAS: 4. Publish the new user in the Admin tab of GAS and/or Supplier with:
        WAS: a. activation checkbox
        WAS: b. Person selection ora add: a GAS_REFERRER_TECH can choose among people in DES without user bound

        WAS: NOTE:
        WAS: Person binding will happen only in 4b. step! User can be bound to an existent Person, or a new one will be created

        Steps:
        1. create (inactive) User
        2. create Place if it does not exist
        3. create Person and link him to the new User
        3. bind User to appropriate role in Supplier and/or GAS
        4. Wait for new registration to be confirmed by user
        5. Send email to GAS_REFERRER_TECH or all GAS_REFERRER_TECHs if the new user is bound to Supplier
        6. Publish the new user in the Admin tab of GAS and/or Supplier with:
            a. activation checkbox
        """


#KO fero: send to new user the confirmation email
#        # 1-Create user
#
#        user = User(
#            username=self.cleaned_data['username'],
#            first_name=self.cleaned_data['name'],
#            last_name=self.cleaned_data['surname'],
#            email=self.cleaned_data['email'],
#        )
#        user.set_password(self.cleaned_data['password1'])
#        user.is_active=False
#        user.save()

        # 1-Create inactive user (to be confirmed by email)
        new_user = RegistrationProfile.objects.create_inactive_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['email'],
            profile_callback=self.profile_callback
        )

    def profile_callback(self, user):

        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['surname']
        user.save()
        
        #2-Create base objects
        place, created = Place.objects.get_or_create(
            city=self.cleaned_data['city'],
            address='', name=''
        )

        try:
            contact_email, created = \
                Contact.objects.get_or_create(flavour="EMAIL", value=self.cleaned_data['email'])
        except Contact.MultipleObjectsReturned as e:
            contacts = Contact.objects.filter(flavour="EMAIL", value=self.cleaned_data['email'])
            contact_email = contacts[0]
            log.warning("Multiple contact found: %s id = %s" % (
                contact_email, map(lambda x : x.pk, contacts))
            )

        try:
            contact_phone, created = \
                Contact.objects.get_or_create(flavour="PHONE", value=self.cleaned_data['phone'])
        except Contact.MultipleObjectsReturned as e:
            contacts = Contact.objects.filter(flavour="PHONE", value=self.cleaned_data['phone'])
            contact_phone = contacts[0]
            log.warning("Multiple contact found: %s id = %s" % (
                contact_phone, map(lambda x : x.pk, contacts))
            )
        
        #3-Create person
        # COMMENT matteo: even if there are already one (or more) persons with the same values (name, 
        # username, place) it is not a problem, the data will be normalized after.

        person = Person(
            name = self.cleaned_data['name'],
            surname = self.cleaned_data['surname'],
            address = place,
            user = user
        )
        person.save()
        person.contact_set.add( contact_email, contact_phone)

        gas = self.cleaned_data.get('gas_choice')
        if gas:

            # COMMENT fero: following our workflow we can't bind person to GAS now
            # we can bind User to role GAS Member for this GAS
            # in the activation phase (4a.) we would perform this step
            gm = GASMember( person=person, gas=gas )
            gm.save()
#            pr = ParamRole.get_role(GAS_MEMBER, gas=gas)
#            ppr = PrincipalParamRoleRelation.objects.create(user=user, role=pr)
#            ppr.save()

            #Send email for GAS_REFERRER_TECH
            techs = gas.tech_referrers_people
            if techs:
                #TODO Matteo: put also 'city' and 'phone' form fields in this email
                body = _("new registration from %(username)s %(usersurname)s with email %(email)s. User active status is %(active)s. Motivation: %(motivation)s...") % {
                    'username' : user.first_name,
                    'usersurname' : user.last_name,
                    'email' : user.email,
                    'active' : user.is_active,
                    'motivation' : self.cleaned_data['motivation'],
                }
                #from notification.models import Notice
                #GAS_REFERRER_TECH
                for tech in techs:
                    #TODO: Notification or send email
                    recipient = tech.user.email
                    recipient = tech.preferred_email_contacts
                    log.debug("Send email for tech %s with body %s" % (recipient, body))
                #FORUM
                #FIXME: not set! Quale è l'email del FORUM del GAS?
                if gas.orders_email_contact:
                    #TODO: Notification or send email
                    forum = gas.orders_email_contact.value
                    log.debug("Send email for FORUM %s with body %s" % (forum, body))

        supplier = self.cleaned_data.get('supplier_choice')
        if supplier:
            pr = ParamRole.get_role(SUPPLIER_REFERRER, supplier=supplier)
            ppr = PrincipalParamRoleRelation.objects.create(user=user, role=pr)
            ppr.save()

        

        

        

