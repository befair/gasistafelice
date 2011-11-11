from django.utils.translation import ugettext, ugettext_lazy as _

SUPPLIER_FLAVOUR_LIST = [
    ('COMPANY', _('Company')),
    ('COOPERATING', _('Cooperating')),
    ('FREELANCE', _('Freelance')),
]

MU_CHOICES = [('Km', 'Km')]
ALWAYS_AVAILABLE = 1000000000

PHONE = 'PHONE'
EMAIL = 'EMAIL'
FAX = 'FAX'

CONTACT_CHOICES = [
    (PHONE, _('PHONE')),
    (EMAIL, _('EMAIL')),
    (FAX, _('FAX')),
]

DAY_CHOICES = [
    ('MONDAY', _('Monday')),
    ('TUESDAY', _('Tuesday')),
    ('WEDNESDAY', _('Wednesday')),
    ('THURSDAY', _('Thursday')),
    ('FRIDAY', _('Friday')),
    ('SATURDAY', _('Saturday')),
    ('SUNDAY', _('Sunday')),
]


