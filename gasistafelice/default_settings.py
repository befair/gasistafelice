# Django settings for gasistafelice project.

import os, locale
import consts
from django.utils.translation import ugettext_lazy as _

DEBUG = True
TEMPLATE_DEBUG = DEBUG
FORM_DEBUG = False
EMAIL_DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages' # change this to a proper location
PROFILING=False

ACCOUNT_ACTIVATION_DAYS = 2
DIGEST_INTERVAL_DAYS = 3

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
VERSION = __version__ = file(os.path.join(PROJECT_ROOT, 'VERSION')).read().strip()

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'des_orders_db',
        'USER': 'des_db_user',
        'PASSWORD': '', 
        'HOST': '',    
        'PORT': '',   
    },
    'super': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'des_orders_db',    
        'USER': 'postgres',   
        'PASSWORD': '',      
        'HOST': '',         
        'PORT': '',        
    },
    'maintenance': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',    
        'USER': 'postgres',   
        'PASSWORD': '',      
        'HOST': '',         
        'PORT': '',        
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

LANGUAGES = (
    ('it', _('Italian')),
    ('sl', _('Slovenian')),
    ('de', _('German')),
    ('en', _('English')),
    ('fr', _('French')),
    ('es', _('Spanish')),
)
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
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'gasistafelice.middleware.ResourceMiddleware',
    'gasistafelice.middleware.UpdateRequestUserMiddleware',
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
    'reversion',
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
    'gasistafelice.des_notification',
    'notification',
    'registration',
    'captcha',
    'ajax_select',
    'south',
    'gdxp',
    #'django.contrib.staticfiles',
]

#INSTALLED_APPS.insert(0, 'django_extensions')


try:
    import rosetta
except ImportError:
    pass
else:
    INSTALLED_APPS.append('rosetta')

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
            'class':'lib.loghandlers.GroupWriteRotatingFileHandler',
            'filename': LOG_FILE,
            'maxBytes': 1024*1024*5,
            'backupCount' : 5,
            'formatter': 'simple'
        },
        'logfile_debug':{
            'level':'DEBUG',
            'class':'lib.loghandlers.GroupWriteRotatingFileHandler',
            'filename': LOG_FILE_DEBUG,
            'maxBytes': 1024*1024*5,
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
        'blocks' : ['balance', 'site_transactions']
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
        'descr': 'Patti',
        'blocks': ['gas_pacts', 'categories'], 
    },{
        'name' : 'info',
        'descr' : 'Scheda del GAS',
        'blocks' : ['gas_details', 'gasmembers'],
    },{
        'name' : 'admin',
        'descr' : 'Admin',
        'blocks' : ['gas_users'],   # 'users' Referrer and roles
    },{
        'name' : 'accounting',
        'descr' : 'Conto',
        'blocks' : ['balance_gas', 'insolutes_orders', 'transactions', 'recharge', 'fee']
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
        'blocks' : ['balance_gm', 'gasmember_transactions']
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
        'name' : 'admin',
        'descr' : 'Admin',
        'blocks' : ['supplier_users'],   # 'users' Referrer and roles
    },{
        'name' : 'accounting',
        'descr' : 'Conto',
        'blocks' : ['balance', 'transactions']
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
        'name' : 'registration',
        'descr': 'Registrazione',
        'blocks': ['order_invoice', 'curtail']
#    },{ 
#        'name' : 'pay',
#        'descr': 'Pagamento',
#        'blocks': ['order_insolute']
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
        'blocks' : ['balance_pact', 'insolutes_orders', 'transactions']
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
    'place' : [{
        'name': 'info',
        'descr': 'Scheda del luogo',
        'blocks' : ['details']
    }],
}


LOGIN_URL = "/%saccounts/login/" % URL_PREFIX
LOGIN_REDIRECT_URL = "/%s" % URL_PREFIX
LOGOUT_URL = "/%saccounts/logout/" % URL_PREFIX
CAN_CHANGE_CONFIGURATION_VIA_WEB = False
ENABLE_OLAP_REPORTS = False

DATE_FMT = "%d/%m/%Y"
LONG_DATE_FMT = "%A %d %B %Y"
MEDIUM_DATE_FMT = "%a %d %b"
MEDIUM_DATETIME_FMT = "%a %d %b %H:%M"
LONG_DATETIME_FMT = "%A %d %B %Y %H:%M"
SHORT_DATE_FMT = "%Y-%m-%d"


# NON FUNZIONA NON CAPISCO COME MAI
#locale.setlocale(locale.LC_ALL, 'it_IT.UTF8')

#DOMTHU:
#locale.setlocale(locale.LC_ALL, 'it_IT.ISO-8859-1')
#locale.setlocale(locale.LC_ALL, 'it_IT.1252')
#locale.setlocale(locale.LC_ALL, 'it_IT')   #by default is .ISO8859-1
#locale.setlocale(locale.LC_ALL, ('it_IT', 'ISO-8859-1'))
#locale.setlocale(locale.LC_ALL, ('it_IT', '1252'))

# From: http://en.wikipedia.org/wiki/Postal_code
# A postal code (known in various countries as a post code, postcode, or ZIP code)
# is a series of letters and/or digits appended to a postal address for the purpose of sorting mail.
#
# DES is a usually a small land, so limit postal codes to validate only if int(zipcode) succeed
# could be a good practice
VALIDATE_NUMERICAL_ZIPCODES = True

INIT_OPTIONS = {
    'domain' : "ordini.desmacerata.it",
    'sitename' : "DES Macerata",
    'sitedescription' : "Gestione degli ordini per il Distretto di Economia Solidale della Provincia di Macerata (DES-MC)",
    'su_username' : "admin",
    'su_name'   : "Referente informatico",
    'su_surname': "del DES-MC",
    'su_email'  : "",
    'su_PASSWORD' : "admin", 
}

MAINTENANCE_MODE = False

# --- WARNING: changing following parameters implies fixtures adaptation --
# Default category for all uncategorized products
DEFAULT_CATEGORY_CATCHALL = 'Non definita' #fixtures/supplier/initial_data.json
JUNK_EMAIL = 'devnull@desmacerata.it'
EMAIL_DEBUG_ADDR = 'gftest@gasistafelice.org'
DEFAULT_SENDER_EMAIL = 'gasistafelice@desmacerata.it'
SUPPORT_EMAIL="dev@gasistafelice.org"

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

#------ CAPTCHA settings

CAPTCHA_FONT_SIZE = 40
APTCHA_LETTER_ROTATION = (-25,25)

#-------------------------------------------------------------------------------
# Ajax_select settings

AJAX_LOOKUP_CHANNELS = {
    'placechannel' : ( 'gasistafelice.base.forms.lookups' , 'PlaceLookup'),
    'personchannel' : ( 'gasistafelice.base.forms.lookups' , 'PersonLookup')
}
# magically include jqueryUI/js/css
AJAX_SELECT_BOOTSTRAP = False
#AJAX_SELECT_INLINES = 'inline'

#STATIC_URL = '/site_static/'
#STATIC_ROOT = PROJECT_ROOT + '/site_static/'

#------------------------------------------------------------------------------
#The path where the profiling files are stored
PROFILE_LOG_BASE = PROJECT_ROOT + '/profiling_logs'

