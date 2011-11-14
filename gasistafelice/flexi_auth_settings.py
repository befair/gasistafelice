
# IMHO it does not work
from django.utils.translation import ugettext_lazy as _
import consts

# TODO: DES_REFERRER role (or remove GAS_REFERRER role?)
ROLES_LIST = (
#    (consts.NOBODY, _('Nobody')),
#    (consts.SUPPLIER_REFERRER, _('Supplier')),
#    (consts.GAS_MEMBER, _('GAS member')),
#    (consts.GAS_REFERRER, _('GAS referrer')),
#    (consts.GAS_REFERRER_SUPPLIER, _('GAS supplier referrer')),
#    (consts.GAS_REFERRER_ORDER, _('GAS order referrer')),
#    (consts.GAS_REFERRER_WITHDRAWAL, _('GAS withdrawal referrer')),
#    (consts.GAS_REFERRER_DELIVERY, _('GAS delivery referrer')),
#    (consts.GAS_REFERRER_CASH, _('GAS cash referrer')),
#    (consts.GAS_REFERRER_TECH, _('GAS technical referrer')),
#    (consts.DES_ADMIN, _('DES administrator')),
    (consts.NOBODY, 'Nessuno'),
    (consts.SUPPLIER_REFERRER, 'Fornitore'),
    (consts.GAS_MEMBER, 'Gasista'),
    (consts.GAS_REFERRER, 'GAS referrer'),
    (consts.GAS_REFERRER_SUPPLIER, 'Referente fornitore'),
    (consts.GAS_REFERRER_ORDER, 'Referente di ordine'),
    (consts.GAS_REFERRER_WITHDRAWAL, 'GAS withdrawal referrer'),
    (consts.GAS_REFERRER_DELIVERY, 'GAS delivery referrer'),
    (consts.GAS_REFERRER_CASH, 'Referente economico'),
    (consts.GAS_REFERRER_TECH, 'Referente informatico'),
    (consts.DES_ADMIN, 'Amministratore del DES'),
)

PARAM_CHOICES = (
   ('des', _('DES')),
   ('gas', _('GAS')),
   ('supplier', _('Supplier')),
   ('pact', _('GAS-supplier solidal pact')),
   ('order', _('GAS-supplier order')),
   ('withdrawal', _('Withdrawal appointment')),
   ('delivery', _('Delivery appointment')),  
)

VALID_PARAMS_FOR_ROLES = {
    ## format
    # ``{<role name>: {<parameter name>: <parameter type>, ..}, ..}``
    # where the parameter type is expressed as a *model label* (i.e. a string of the form ``app_label.model_name``)
    consts.SUPPLIER_REFERRER : {'supplier':'supplier.Supplier'},
    consts.GAS_MEMBER : {'gas':'gas.GAS'},
    consts.GAS_REFERRER : {'gas':'gas.GAS'},
    consts.GAS_REFERRER_CASH : {'gas':'gas.GAS'},
    consts.GAS_REFERRER_TECH : {'gas':'gas.GAS'},
    consts.GAS_REFERRER_SUPPLIER : {'pact':'gas.GASSupplierSolidalPact'}, 
    consts.GAS_REFERRER_ORDER : {'order':'gas.GASSupplierOrder'},
    consts.GAS_REFERRER_WITHDRAWAL: {'withdrawal':'gas.Withdrawal'},
    consts.GAS_REFERRER_DELIVERY: {'delivery':'gas.Delivery'},
    consts.DES_ADMIN: {'des':'des.DES'},                         
}

