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
            'base.backends.AuthenticationParamRoleBackend',
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
DATETIME_INPUT_FORMATS = ('%m/%d/%Y %H:%M', '%Y-%m-%d %H:%M:%S', 
'%Y-%m-%d %H:%M', '%Y-%m-%d', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y',
'%m/%d/%y %H:%M:%S', '%m/%d/%y %H:%M', '%m/%d/%y')
TIME_INPUT_FORMATS = ('%H:%M', '%H:%M:%S')
DATE_INPUT_FORMATS = ('%d/%m/%Y', '%Y-%m-%d', '%m/%d/%y', '%b %d %Y',
'%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y',
'%B %d, %Y', '%d %B %Y', '%d %B, %Y')

DECIMAL_SEPARATOR = '.'
THOUSAND_SEPARATOR = ' '

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
#    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'gasistafelice.urls'

TEMPLATE_DIRS = (
    PROJECT_ROOT + "/rest/templates",
    PROJECT_ROOT + "/templates",
)

INSTALLED_APPS = [
    'permissions',
    'workflows',
    'history',
    'flexi_auth',
    'simple_accounting',
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
    'notification',
    'gasistafelice.des_notification',
    'registration',
    'captcha',
    #'south',
]

FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, 'fixtures/auth/'),
    os.path.join(PROJECT_ROOT, 'fixtures/base/'),
    os.path.join(PROJECT_ROOT, 'fixtures/des/'),
    os.path.join(PROJECT_ROOT, 'fixtures/supplier/'),
    os.path.join(PROJECT_ROOT, 'fixtures/gas/'),
)

LOG_FILE = os.path.join(PROJECT_ROOT, 'gf.log')
LOG_FILE_DEBUG = os.path.join(PROJECT_ROOT, 'gf_debug.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'logfile':{
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,
            'maxBytes': 1048576,
            'backupCount' : 5,
            'formatter': 'simple'
        },
        'logfile_debug':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_DEBUG,
            'maxBytes': 1048576,
            'backupCount' : 10,
            'formatter': 'verbose'
        },
#        'mail_admins': {
#            'level': 'ERROR',
#            'class': 'django.utils.log.AdminEmailHandler',
#        }
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
        'gasistafelice': {
            'handlers': ['console', 'logfile', 'logfile_debug'],
            'level': 'DEBUG',
        }
    }
}

THEME = "milky"
AUTH_PROFILE_MODULE = 'users.UserProfile'
URL_PREFIX = "gasistafelice/"

RESOURCE_PAGE_BLOCKS = {
    'site' : [{
        'name' : 'people',
        'descr' : 'Partecipanti',
        'blocks' : ['gas_list', 'suppliers_report', 'persons']  #, 'suppliers'
    },{
        'name' : 'order',
        'descr' : 'Ordini',
        'blocks' : ['open_orders', 'des_pacts']
    },{
        'name' : 'info',
        'descr' : 'Scheda del DES',
        'blocks' : ['details', 'categories']
    },{
        'name' : 'accounting',
        'descr' : 'Conto',
        'blocks' : ['transactions']
    },{
        'name' : 'archive',
        'descr' : 'Archivio',
        'blocks' : ['stored_orders']
    }],
    'gas' : [{
        'name' : 'orders',
        'descr': 'Ordini',
        'blocks': ['open_orders', 'closed_orders', 'prepared_orders'], 
    },{
        'name' : 'suppliers',
        'descr': 'Fornitori',
        'blocks': ['gas_pacts', 'categories'], 
    },{
        'name' : 'info',
        'descr' : 'Scheda del GAS',
        'blocks' : ['gas_details', 'gasmembers']
    },{
        'name' : 'accounting',
        'descr' : 'Conto',
        'blocks' : ['transactions', 'recharge', 'fee'] #Finalize Orders, transactions explode in Transact_Casa, Transact_Borselino
    },{
        'name' : 'archive',
        'descr' : 'Archivio',
        'blocks' : ['stored_orders'] #TODO transactions for Transact_gasmembers, Transact_suppliers
    }],
    'gasmember': [{
        'name' : 'orders',
        'descr': 'Ordinare',
        'blocks': ['order'], #This can be filtered in order block, 'open_orders','closed_orders'],
    },{
        'name' : 'basket',
        'descr' : 'Paniere',
        'blocks' : ['basket', 'basket_sent']
    },{
        'name' : 'info',
        'descr' : 'Scheda del gasista',
        'blocks' : ['gasmember_details', 'person_details']
    },{
        'name' : 'accounting',
        'descr' : 'Conto',
        'blocks' : ['transactions']
    }],
    'supplier' : [{
        'name' : 'products',
        'descr': 'Prodotti',
        'blocks': ['stocks']
    },{
        'name' : 'orders',
        'descr': 'Ordini',
        'blocks': ['open_orders', 'prepared_orders', 'supplier_pacts']
    },{
        'name' : 'info',
        'descr': 'Scheda del fornitore',
        'blocks': ['supplier_details', 'categories', 'closed_orders']
    },{
        'name' : 'accounting',
        'descr' : 'Conto',
        'blocks' : ['transactions']
    },{
        'name' : 'archive',
        'descr' : 'Archivio',
        'blocks' : ['stored_orders']
    }],
    'order' : [{ 
        'name' : 'info',
        'descr': 'Ordine',
        'blocks': ['order_details', 'order_report']
    },{ 
        'name' : 'delivery',
        'descr': 'Pagamento',
        'blocks': ['order_invoice', 'curtail', 'order_insolute']
    }],

    'person' : [{
        'name': 'info',
        'descr': 'Scheda della persona',
        'blocks' : ['person_details', 'person_gasmembers']
    }],

    'pact' : [{ 
        'name' : 'stock',
        'descr': 'Prodotti',
        'blocks': ['open_orders', 'gasstocks']
    },{
        'name': 'info',
        'descr': 'Scheda del patto',
        'blocks' : ['pact_details', 'closed_orders']
    },{
        'name' : 'accounting',
        'descr' : 'Conto',
        'blocks' : ['transactions']
    },{
        'name' : 'archive',
        'descr' : 'Archivio',
        'blocks' : ['stored_orders']
    }],
    'stock' : [{
        'name': 'info',
        'descr': 'Scheda del prodotto',
        'blocks' : ['stock_details', 'open_orders']
    }],
}


LOGIN_URL = "/%saccounts/login/" % URL_PREFIX
LOGIN_REDIRECT_URL = "/%s" % URL_PREFIX
LOGOUT_URL = "/%saccounts/logout/" % URL_PREFIX
CAN_CHANGE_CONFIGURATION_VIA_WEB = False
ENABLE_OLAP_REPORTS = False

DATE_FMT = "%d/%m/%Y"
LONG_DATE_FMT = "%A %d %B %Y"
MEDIUM_DATETIME_FMT = "%D %d %b %Y %H:%M"

locale.setlocale(locale.LC_ALL, 'it_IT.UTF8')
#DOMTHU:
#locale.setlocale(locale.LC_ALL, 'it_IT.ISO-8859-1')
#locale.setlocale(locale.LC_ALL, 'it_IT.1252')
#locale.setlocale(locale.LC_ALL, 'it_IT')   #by default is .ISO8859-1
#locale.setlocale(locale.LC_ALL, ('it_IT', 'ISO-8859-1'))
#locale.setlocale(locale.LC_ALL, ('it_IT', '1252'))

INIT_OPTIONS = {
    'domain' : "ordini.desmacerata.it",
    'sitename' : "DES Macerata",
    'sitedescription' : "Gestione degli ordini per il Distretto di Economia Solidale della Provincia di Macerata (DES-MC)",
    'su_username' : "admin",
    'su_name'   : "Referente informatico",
    'su_surname': "del DES-MC",
    'su_email'  : "",
    'su_passwd' : "admin",
}

# --- WARNING: changing following parameters implies fixtures adaptation --
# Default category for all uncategorized products
DEFAULT_CATEGORY_CATCHALL = 'Non definita' #fixtures/supplier/initial_data.json
JUNK_EMAIL = 'devnull@desmacerata.it'

# Superuser username

#------ AUTH settings
from flexi_auth_settings import *

#------ ACCOUNTING settings
from simple_accounting_settings import *

#------ NOTIFICATION settings

DEFAULT_FROM_EMAIL = "gasistafelice@desmacerata.it"
NOTIFICATION_BACKENDS = (
    ("email", "notification.backends.email.EmailBackend"),
)

CAPTCHA_FONT_SIZE = 40
APTCHA_LETTER_ROTATION = (-25,25)
