# Django settings for gasistafelice project.

import os
def bool_from_env(key):
    var = os.getenv(key)
    if not var:
        return None
    if var.upper() in ("Y", "TRUE", "ON", "1"):
        return True
    return False

from default_settings import *

DEBUG = bool_from_env("DJANGO_DEBUG")
TEMPLATE_DEBUG = DEBUG
FORM_DEBUG = False
EMAIL_DEBUG = DEBUG

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = '/tmp/app-messages' # change this to a proper location
else:
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = os.getenv("EMAIL_PORT")
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = bool_from_env("EMAIL_USE_TLS")
    EMAIL_USE_SSL = bool_from_env("EMAIL_USE_SSL")
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("POSTGRES_NAME"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"), 
        'HOST': os.getenv("POSTGRES_HOST"),    
        #'PORT': '',   
    },
    # 'super': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'des_orders_db',    
    #     'USER': 'postgres',   
    #     'PASSWORD': '',      
    #     'HOST': '',         
    #     'PORT': '',        
    # },
    # 'maintenance': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'postgres',    
    #     'USER': 'postgres',   
    #     'PASSWORD': '',      
    #     'HOST': '',         
    #     'PORT': '',        
    # }
}

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        # "level": "DEBUG" if DEBUG else "INFO",
        "level": "INFO",
    },
}

#locale.setlocale(locale.LC_ALL, 'it_IT.UTF8')

