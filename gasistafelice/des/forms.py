# -*- coding: utf-8 -*-

from registration.forms import RegistrationFormUniqueEmail
from django import forms
from django.db import transaction
from django.contrib.auth.models import User

from captcha.fields import CaptchaField

from flexi_auth.models import ParamRole, PrincipalParamRoleRelation
from gasistafelice.consts import SUPPLIER_REFERRER

from gasistafelice.gas.models import GAS, GASMember
from gasistafelice.supplier.models import Supplier
from gasistafelice.base.models import Place, Contact, Person

class DESRegistrationForm(RegistrationFormUniqueEmail):

    gas_choice = forms.ModelChoiceField(
        label="Sei del gas...",
        queryset = GAS.objects.all(),
        required=False
    )
    supplier_choice = forms.ModelChoiceField(
        label="Sei il fornitore...",
        queryset = Supplier.objects.all(),
        required=False
    )

    name = forms.CharField( label="Nome")
    surname = forms.CharField( label="Cognome")
    city = forms.CharField(label="Città")
    phone = forms.CharField(
        label="Numero di telefono",
        required=True,
        help_text="È importante poter contattare chi si registra via telefono"
    )
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

        # Create base objects
        place, created = Place.objects.get_or_create(
            city=self.cleaned_data['city'],
            address='', name=''
        )

        contact_email, created = \
            Contact.objects.get_or_create(flavour="EMAIL", value=self.cleaned_data['email'])

        contact_phone, created = \
            Contact.objects.get_or_create(flavour="PHONE", value=self.cleaned_data['phone'])

        # Create user

        user = User(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['name'],
            last_name=self.cleaned_data['surname'],
            email=self.cleaned_data['email'],
        )
        user.set_password(self.cleaned_data['password1'])
        user.is_active=False
        user.save()

        # Create person

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
            gm = GASMember( person=person, gas=gas )
            gm.save()

        supplier = self.cleaned_data.get('supplier_choice')
        if supplier:
            pr = ParamRole.get_role(SUPPLIER_REFERRER, supplier=supplier)
            ppr = PrincipalParamRoleRelation.objects.create(
                user=user, role=pr
            )
            ppr.save()

        

        

        

