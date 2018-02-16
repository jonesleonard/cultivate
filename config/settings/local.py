from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hansberry',
        'USER': 'sa',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}