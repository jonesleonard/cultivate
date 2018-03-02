from .base import *

DEBUG = True

# logs any emails sent to the console
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

