from django.utils.translation import ugettext, ugettext_lazy as _

STATES_LIST = [
    ('OPEN', _('open')),
    ('CLOSED', _('closed')),
    ('PENDING', _('pending')),
    ('SENT', _('sent')),
    ('DELIVERED', _('delivered')),
    ('ULTIMATED', _('ultimated')),
]

NOBODY = 'NOBODY'
SUPPLIER_REFERRER = 'SUPPLIER_REFERRER'
GAS_MEMBER = 'GAS_MEMBER'
GAS_REFERRER_SUPPLIER = 'GAS_REFERRER_SUPPLIER'
GAS_REFERRER_ORDER = 'GAS_REFERRER_ORDER'
GAS_REFERRER_WITHDRAW = 'GAS_REFERRER_WITHDRAW'
GAS_REFERRER_DELIVERY = 'GAS_REFERRER_DELIVERY'
GAS_REFERRER_CASH = 'GAS_REFERRER_CASH'
GAS_REFERRER_TECH = 'GAS_REFERRER_TECH'
SUPPLIER_REFERRER = 'SUPPLIER_REFERRER'

ROLES_LIST = [
(NOBODY, _('Nobody')),
(SUPPLIER_REFERRER, _('Supplier referrer')),
(GAS_MEMBER, _('GAS member')),
(GAS_REFERRER_SUPPLIER, _('GAS supplier referrer')),
(GAS_REFERRER_ORDER, _('GAS order referrer')),
(GAS_REFERRER_WITHDRAW, _('GAS withdrawal referrer')),
(GAS_REFERRER_DELIVERY, _('GAS delivery referrer')),
(GAS_REFERRER_CASH, _('GAS cash referrer')),
(GAS_REFERRER_TECH, _('GAS technical referrer')),
]

SUPPLIER_FLAVOUR_LIST = [
('COMPANY', _('Company')),
('COOPERATING', _('Cooperating')),
]

MU_CHOICES = [('Km', 'Km')]
ALWAYS_AVAILABLE = 1000000000

CONTACT_CHOICES = [
('PHONE', _('PHONE')),
('EMAIL', _('EMAIL')),
('FAX', _('FAX')),
]
