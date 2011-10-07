# Django settings for gasistafelice project.

import os, locale
import consts
from django.utils.translation import ugettext_lazy as _

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
VERSION = __version__ = file(os.path.join(PROJECT_ROOT, 'VERSION')).read().strip()

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'flexi_auth.backends.ParamRoleBackend',
        )

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'it'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '26lk413y7^-z^t$#u(xh4uv@+##0jh)&_wxzqho655)eux33@k'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'gasistafelice.middleware.ResourceMiddleware',
)

ROOT_URLCONF = 'gasistafelice.urls'

TEMPLATE_DIRS = (
    PROJECT_ROOT + "/rest/templates",
    PROJECT_ROOT + "/templates",
)

INSTALLED_APPS = (
    'permissions',
    'workflows',
    'history',
    'flexi_auth',
    'accounting',
    'gasistafelice.base',
    'gasistafelice.supplier',
    'gasistafelice.gas',
    'gasistafelice.admin',
    'gasistafelice.gas_admin',
    'gasistafelice.rest',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'gasistafelice.des',
    'gasistafelice.users',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.comments',
    'gasistafelice.localejs',
    #'south',
    
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, 'fixtures/auth/'),
    os.path.join(PROJECT_ROOT, 'fixtures/base/'),
    os.path.join(PROJECT_ROOT, 'fixtures/des/'),
    os.path.join(PROJECT_ROOT, 'fixtures/gas/'),
    os.path.join(PROJECT_ROOT, 'fixtures/supplier/'),
)

THEME = "milky"
AUTH_PROFILE_MODULE = 'users.UserProfile'
URL_PREFIX = "gasistafelice/"

RESOURCE_PAGE_BLOCKS = {
    'site' : [{
        'name' : 'people',
        'descr' : 'Partecipanti',
        'blocks' : ['gas_list', 'suppliers', 'persons']
    },{
        'name' : 'order',
        'descr' : 'Ordini',
        'blocks' : ['open_orders']
    },{
        'name' : 'info',
        'descr' : 'Scheda del DES',
        'blocks' : ['details', 'categories']
    }],
    'gas' : [{
        'name' : 'orders',
        'descr': 'Ordini',
        'blocks': ['open_orders', 'closed_orders'], #products_to_order for GAS with GASConfig that want to show only one available order/delivery?
    },{
        'name' : 'suppliers',
        'descr': 'Fornitori',
        'blocks': ['pacts', 'categories'], #categorie presenti sul des ma non acquistate dal GAS
    },{
        'name' : 'info',
        'descr' : 'Scheda del GAS',
        'blocks' : ['details', 'gasmembers']
    }],
    'gasmember': [{
        'name' : 'orders',
        'descr': 'Ordinare',
        'blocks': ['order'], #This can be filtered in order block, 'open_orders','closed_orders'],
    },{
        'name' : 'basket',
        'descr' : 'Paniere',
        'blocks' : ['basket']
    },{
        'name' : 'info',
        'descr' : 'Scheda del gasista',
        'blocks' : ['details']
    },{
        'name' : 'accounting',
        'descr' : 'Conto',
        'blocks' : []
    }], #must be extended with economic section
    'supplier' : [{
        'name' : 'products',
        'descr': 'Prodotti',
        'blocks': ['stocks'],
    },{
        'name' : 'orders',
        'descr': 'Ordini',
        'blocks': ['open_orders', 'closed_orders'],
    },{
        'name' : 'info',
        'descr': 'Scheda del fornitore',
        'blocks': ['details', 'categories'],
    }], #must be extended with economic section
    'order' : [{ 
        'name' : 'info',
        'descr': 'Ordine',
        'blocks': ['details', 'order_report'],
    },{ 
        'name' : 'delivery',
        'descr': 'Consegna',
        'blocks': [],
    }],

    'pact' : [{
        'name': 'info',
        'descr': 'Info',
        'blocks' : ['details', 'open_orders', 'closed_orders'],
    },{ 
        'name' : 'stock',
        'descr': 'Prodotti',
        'blocks': ['gasstocks'],
    }],
}
   
LOGIN_URL = "/%saccounts/login/" % URL_PREFIX
LOGIN_REDIRECT_URL = "/%s" % URL_PREFIX
LOGOUT_URL = "/%saccounts/logout/" % URL_PREFIX
CAN_CHANGE_CONFIGURATION_VIA_WEB = False
ENABLE_OLAP_REPORTS = False

DATE_FMT = "%d/%m/%Y"
locale.setlocale(locale.LC_ALL, 'it_IT.UTF8')


#--------------------- AUTH settings ----------------#
## QUESTION: Maybe app-specific settings like these should be placed 
## in an dedicated settings module and imported here ?

# TODO: DES_REFERRER role (or remove GAS_REFERRER role?)
ROLES_LIST = (
    (consts.NOBODY, _('Nobody')),
    (consts.SUPPLIER_REFERRER, _('Supplier')),
    (consts.GAS_MEMBER, _('GAS member')),
    (consts.GAS_REFERRER, _('GAS referrer')),
    (consts.GAS_REFERRER_SUPPLIER, _('GAS supplier referrer')),
    (consts.GAS_REFERRER_ORDER, _('GAS order referrer')),
    (consts.GAS_REFERRER_WITHDRAWAL, _('GAS withdrawal referrer')),
    (consts.GAS_REFERRER_DELIVERY, _('GAS delivery referrer')),
    (consts.GAS_REFERRER_CASH, _('GAS cash referrer')),
    (consts.GAS_REFERRER_TECH, _('GAS technical referrer')),
    (consts.DES_ADMIN, _('DES administrator')),
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

## QUESTION: Does the section below is useful/needed by some pieces of code in *Gasista Felice* ?
PERMISSIONS_CHOICES = (
    (consts.VIEW, _('View')),
    (consts.LIST, _('List')),
    (consts.CREATE, _('Create')),
    (consts.EDIT, _('Edit')),
    (consts.EDIT_MULTIPLE, _('Edit multiple')),
    (consts.DELETE, _('Delete')),
    (consts.ALL, _('All')), # catchall
)

#--------------------- ACCOUNTING settings ----------------#
SUBJECTIVE_MODELS = (
    'gas.GAS',
    'gas.GASMember',
    'supplier.Supplier',                      
)

ACCOUNT_TYPES = (
    (consts.INCOME, _('Incomes')),
    (consts.EXPENSE, _('Expenses')),
    (consts.ASSET, _('Assets')),
    (consts.LIABILITY, _('Liabilities')),
    (consts.EQUITY, _('Equity')),     
)

TRANSACTION_TYPES = (
     (consts.INVOICE_PAYMENT, 'Payment of an invoice '),
     (consts.INVOICE_COLLECTION, 'Collection of an invoice'),
     (consts.GAS_MEMBER_RECHARGE, _('Re-charge from a GAS member')),
     (consts.MEMBERSHIP_FEE_PAYMENT, _('Payment of annual membership fee by a GAS member')),
)
