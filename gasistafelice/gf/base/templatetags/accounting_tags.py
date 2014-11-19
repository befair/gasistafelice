from django import template
from django.conf import settings
from django.template import resolve_variable, loader
from django.template import TemplateSyntaxError
from django.template.loader import get_template, select_template
from django.template.defaultfilters import stringfilter

from django.db import models
import datetime, os.path

from django.utils.translation import ugettext as _

import simple_accounting

register = template.Library()

@register.simple_tag
def human_readable_kind(kind):
    if kind == 'GAS_WITHDRAWAL':
        return _("Curtail")
    elif kind == 'RECHARGE':
        return _("Recharge")
    elif kind == 'MEMBERSHIP_FEE':
        return _("Fee")
    elif kind == 'PAYMENT':
        return _("Payment")
    elif kind == 'REFUND':
        return _("Collect")
    elif kind in ('PACT_EXTRA', 'GAS_EXTRA'):
        return _("Adjustement")
    else:
        return kind

@register.simple_tag
def human_readable_account(account):
    """
    return one string containing the ressource name and the resource urn

    The string is separated by '@@' keyword
    in order to be split and use by jQuery.Resource(_url, _name);
    we expect value.name as ressource-type-pk
    """
    #FIXME: this view must import and know the model controller!!!! (not MVC)
    name = ""
    urn = ""
    if 'person-' in account.name:
        #from gf.gas.models.base import GASMember
        from gf.base.models import Person
        p_pk = account.name.replace("person-", "")
        try:
            obj = Person.objects.get(pk=p_pk)
        except GASMember.DoesNotExist:
            pass
        else:
            name = obj.report_name
            urn = obj.urn

    elif 'gas-' in account.name:
        from gf.gas.models.base import GAS
        p_pk = account.name.replace("gas-", "")
        try:
            obj = GAS.objects.get(pk=p_pk)
        except GAS.DoesNotExist:
            pass
        else:
            name = obj.id_in_des
            urn = obj.urn

    elif 'supplier-' in account.name:
        from gf.supplier.models import Supplier
        p_pk = account.name.replace("supplier-", "")
        try:
            obj = Supplier.objects.get(pk=p_pk)
        except Supplier.DoesNotExist:
            pass
        else:
            name = obj.name
            urn = obj.urn

    if name == "" or urn == "":
        obj = account.system.owner.instance
        name = obj
        #if 'person' in account.name:
        #FIXME: Caught NotImplementedError while rendering: class: GAS method: person
        #because we retrieve ledgerEntries from gf.gas.account
        urn = obj.urn

    return "%(name)s|%(urn)s" % {'name': name, 'urn': urn}

@register.simple_tag
def human_readable_account_csv(account):
    """
        Return one string containing the resource
    """
    name = ""
    if 'person-' in account.name:
        from gasistafelice.base.models import Person
        p_pk = account.name.replace("person-", "")
        try:
            obj = Person.objects.get(pk=p_pk)
        except GASMember.DoesNotExist:
            pass
        else:
            name = obj.report_name

    elif 'gas-' in account.name:
        from gasistafelice.gas.models.base import GAS
        p_pk = account.name.replace("gas-", "")
        try:
            obj = GAS.objects.get(pk=p_pk)
        except GAS.DoesNotExist:
            pass
        else:
            name = obj.id_in_des

    elif 'supplier-' in account.name:
        from gasistafelice.supplier.models import Supplier
        p_pk = account.name.replace("supplier-", "")
        try:
            obj = Supplier.objects.get(pk=p_pk)
        except Supplier.DoesNotExist:
            pass
        else:
            name = obj.name

    if name == "":
        name = "%s" % account.system.owner.instance

    return "%(name)s " % {'name': name.encode("utf-8", "ignore")}

@register.simple_tag
def signed_ledger_entry_amount(ledger_entry):

    if ledger_entry.account.is_stock:

        signed_amount = ledger_entry.amount

    elif ledger_entry.account.base_type == \
        simple_accounting.models.AccountType.EXPENSE:

        signed_amount = +ledger_entry.amount

    elif ledger_entry.account.base_type == \
        simple_accounting.models.AccountType.INCOME:

        signed_amount = -ledger_entry.amount

    return signed_amount
