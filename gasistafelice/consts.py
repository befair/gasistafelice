# -*- coding: utf-8 -*-

## role-related constants
NOBODY = 'NOBODY'
GAS_MEMBER = 'GAS_MEMBER'
GAS_REFERRER = 'GAS_REFERRER'
GAS_REFERRER_SUPPLIER = 'GAS_REFERRER_SUPPLIER'
GAS_REFERRER_CASH = 'GAS_REFERRER_CASH'
GAS_REFERRER_TECH = 'GAS_REFERRER_TECH'
SUPPLIER_REFERRER = 'SUPPLIER_REFERRER'
DES_ADMIN = 'DES_ADMIN'

## QUESTION: Does the section below is useful/needed by some pieces of code in *Gasista Felice* ?

## permission-related constants
VIEW = 'view'
LIST = 'list'
CREATE = 'create'
EDIT = 'edit'
DELETE = 'delete'
ALL = 'all' # catchall
EDIT_MULTIPLE = 'edit_multiple'
CONFIRM = 'confirm'
CASH = 'cash'
VIEW_CONFIDENTIAL = 'view_confidential'

## accounting-related constants
NONDES_NAME = 'NonDES'
NONDES_SURNAME = 'Account'
# account types
INCOME = 'INCOME'
EXPENSE = 'EXPENSE'
ASSET = 'ASSET'
LIABILITY = 'LIABILITY'
EQUITY = 'EQUITY'

# transaction types
INVOICE_PAYMENT = 'INVOICE_PAYMENT'
INVOICE_COLLECTION = 'INVOICE_COLLECTION'
GAS_MEMBER_RECHARGE = 'GAS_MEMBER_RECHARGE'
MEMBERSHIP_FEE_PAYMENT = 'MEMBERSHIP_FEE_PAYMENT' 

# confidential text for blocks
CONFIDENTIAL_VERBOSE_TEXT = """
<div style="padding:1%; font-size: 1.3em; text-align:justify; color: red; line-height:1.5;">
Si è ritenuto opportuno non visualizzare questo blocco
per rispettare la privacy delle persone. Tale scelta se necessario, 
come <a href="http://www.jagom.org/trac/reesgas/query?status=assigned&status=new&status=reopened&type=politico-strategico&or&keywords=~politico&col=id&col=summary&col=status&col=type&col=priority&col=milestone&col=component&order=priority">altre scelte politiche e strategiche del software</a>, 
potrà essere ridiscussa nel tavolo del DES.</div>
"""
