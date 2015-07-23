from .settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': PROJECT_ROOT + '/db/des_import3.db',
        'NAME': 'gf_desmc',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'super': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2'
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
