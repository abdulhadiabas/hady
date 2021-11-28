# -*- coding: utf-8 -*-

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'deep',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
	'CONN_MAX_AGE': 600,
    }
}

#URLS
STATIC_URL = 'https://tehrantek.com/static/'
MEDIA_URL = 'https://tehrantek.com/media/'

