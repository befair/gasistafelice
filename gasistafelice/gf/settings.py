"""
Django settings for gasistafelice project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""


import os
import locale
import consts

from django.utils.translation import ugettext_lazy as _


ENV = os.getenv('APP_ENV', 'dev')

if ENV == 'prod':
    DEBUG = False
    TEMPLATE_DEBUG = False
    EMAIL_DEBUG = False
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

elif ENV == 'stage':
    DEBUG = True
    TEMPLATE_DEBUG = True
    EMAIL_DEBUG = True
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

else:
    DEBUG = True
    TEMPLATE_DEBUG = True
    EMAIL_DEBUG = True
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

FORM_DEBUG = False
EMAIL_FILE_PATH = os.getenv('APP_EMAIL_FILE_PATH', '/dev/stdout')
PROFILING = os.getenv('APP_PROFILING', False)

ACCOUNT_ACTIVATION_DAYS = 2

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
VERSION = __version__ = file(os.path.join(PROJECT_ROOT, 'VERSION')).read().strip()

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DBNAME', 'app'),
        'USER': os.getenv('POSTGRES_USER', 'app'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'app'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': os.getenv('POSTGRES_PORT', 5432),
    }
}

AUTHENTICATION_BACKENDS = (
    'gf.base.backends.AuthenticationParamRoleBackend',
    'flexi_auth.backends.ParamRoleBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}

JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_VERIFY_EXPIRATION': False,
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Rome'
USE_TZ = True

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
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '26lk413y7^-z^t$#u(xh4uv@+##0jh)&_wxzqho655)eux33@k'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.ResourceMiddleware',
    'middleware.UpdateRequestUserMiddleware',
#    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'gf.urls'

TEMPLATE_DIRS = (
    PROJECT_ROOT + "/rest/templates",
    PROJECT_ROOT + "/templates",
)

# MUST BE A LIST IN ORDER TO APPEND APPS (see django-rosetta below)
INSTALLED_APPS = [
    'permissions',
    'workflows',
    #'history',
    'reversion',
    'flexi_auth',
    'simple_accounting',
    'gf.base',
    'gf.supplier',
    'gf.gas',
    #'admin',
    'rest',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'des',
    'users',
    'django.contrib.messages',
    'django.contrib.admin',
    #'django.contrib.comments',
    'django_comments',
    'django.contrib.staticfiles',
    'localejs',
    #TO DJ17'des_notification',
    #TO DJ17'notification',
    #TO DJ17'registration',
    'captcha',
    'ajax_select',
    'gdxp',
    'rest_framework',
    'rest_framework.authtoken',
    'api_v1',
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

LOG_FILE = os.getenv('APP_LOG_FILE', '/dev/stdout')
LOG_FILE_DEBUG = os.getenv('APP_LOG_FILE_DEBUG', '/dev/stdout')

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


LOGIN_URL = "/gasistafelice/accounts/login/"
LOGIN_REDIRECT_URL = "/gasistafelice"
LOGOUT_URL = "/gasistafelice/accounts/logout/"
CAN_CHANGE_CONFIGURATION_VIA_WEB = False
ENABLE_OLAP_REPORTS = False

DATE_FMT = "%d/%m/%Y"
LONG_DATE_FMT = "%A %d %B %Y"
MEDIUM_DATE_FMT = "%a %d %b"
MEDIUM_DATETIME_FMT = "%a %d %b %H:%M"
LONG_DATETIME_FMT = "%A %d %B %Y %H:%M"
SHORT_DATE_FMT = "%Y-%m-%d"


locale.setlocale(locale.LC_ALL, os.getenv('APP_LOCALE', 'it_IT.UTF-8'))
#DOMTHU:
#locale.setlocale(locale.LC_ALL, 'it_IT.ISO-8859-1')
#locale.setlocale(locale.LC_ALL, 'it_IT.1252')
#locale.setlocale(locale.LC_ALL, 'it_IT')   #by default is .ISO8859-1
#locale.setlocale(locale.LC_ALL, ('it_IT', 'ISO-8859-1'))
#locale.setlocale(locale.LC_ALL, ('it_IT', '
# From: http://en.wikipedia.org/wiki/Postal_code
# A postal code (known in various countries as a post code, postcode, or ZIP code)
# is a series of letters and/or digits appended to a postal address for the purpose of sorting mail.
#
# DES is a usually a small land, so limit postal codes to validate only if int(zipcode) succeed
# could be a good practice
VALIDATE_NUMERICAL_ZIPCODES = True

INIT_OPTIONS = {
    'domain':          '{}:{}'.format(
        os.getenv('APP_SERVER_NAME', 'ordini.desmacerata.it'),
        os.getenv('APP_HTTP_PORT', '80'),
    ),
    'sitename':        os.getenv('APP_SITE_NAME', 'DES Macerata'),
    'sitedescription': os.getenv('APP_SITE_DESC', "Gestione degli ordini per il Distretto di Economia Solidale della Provincia di Macerata (DES-MC)"),
    'su_username':     os.getenv('APP_ADMIN_USER', 'admin'),
    'su_name':         os.getenv('APP_ADMIN_NAME', 'Referente informatico'),
    'su_surname':      os.getenv('APP_ADMIN_SURNAME', 'del DES-MC'),
    'su_email':        os.getenv('APP_ADMIN_EMAIL', ''),
    'su_PASSWORD':     os.getenv('APP_ADMIN_PW', 'admin'),
}

MAINTENANCE_MODE = os.getenv('APP_MAINTENANCE_MODE', False)

# --- WARNING: changing following parameters implies fixtures adaptation --
# Default category for all uncategorized products
DEFAULT_CATEGORY_CATCHALL = 'Non definita' #fixtures/supplier/initial_data.json
JUNK_EMAIL = 'devnull@desmacerata.it'
EMAIL_DEBUG_ADDR = os.getenv('APP_EMAIL_DEBUG_ADDR', 'gftest@gasistafelice.org')
DEFAULT_SENDER_EMAIL = 'gasistafelice@desmacerata.it'
SUPPORT_EMAIL="dev@gasistafelice.org"

# Superuser username

#------ AUTH settings
from flexi_auth_settings import *

#------ ACCOUNTING settings
from simple_accounting_settings import *

#------ NOTIFICATION settings
DEFAULT_FROM_EMAIL = os.getenv('APP_DEFAULT_FROM_EMAIL', 'gasistafelice@desmacerata.it')
NOTIFICATION_BACKENDS = (
    ("email", "notification.backends.email.EmailBackend"),
)

#------ CAPTCHA settings
CAPTCHA_FONT_SIZE = 40
APTCHA_LETTER_ROTATION = (-25,25)

#-------------------------------------------------------------------------------
# Ajax_select settings

AJAX_LOOKUP_CHANNELS = {
    'placechannel' : ( 'gf.base.forms.lookups' , 'PlaceLookup'),
    'personchannel' : ( 'gf.base.forms.lookups' , 'PersonLookup')
}
# magically include jqueryUI/js/css
AJAX_SELECT_BOOTSTRAP = False
#AJAX_SELECT_INLINES = 'inline'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'final_static')

#------------------------------------------------------------------------------
#The path where the profiling files are stored
PROFILE_LOG_BASE = os.getenv('APP_PROFILE_LOG_BASE', '/tmp')
