from .base import *

DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hansberry',
        'USER': 'sa',
        'PASSWORD': 'commode-misjudge-stocky-enclose-font-shavuot',
        'HOST': 'localhost',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    }
}