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
        'NAME': os.environ.get('DB_NAME', 'scitweets'),
        'USER': os.environ.get('DB_USERNAME', 'macintosh'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'macintosh'),
        'HOST': os.environ.get('LOCAL_DB_IP', 'localhost'),                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': os.environ.get('LOCAL_DB_PORT', ''),
    }
}


# Rosetta
ROSETTA_WSGI_AUTO_RELOAD = True