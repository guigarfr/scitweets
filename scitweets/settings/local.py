import os
from common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r^^3n&5tm(qis0$h3g)l=ob*8%e)8==o!4!yxg@-a)02s1pka5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS += (
    'djangobower',
)

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'scitweets',
        'USER': 'macintosh',
        'PASSWORD': '',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': '',
    }
}

# # Parse database configuration from $DATABASE_URL
# import dj_database_url
# DATABASES['default'] =  dj_database_url.config(default='postgres://macintosh@localhost:5432/scitweets')
#


