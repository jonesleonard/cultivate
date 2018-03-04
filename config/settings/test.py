from .base import *

DEBUG = True

TEMPLATES += [
    {
        'OPTIONS':
        'string_if_invalid': 'INVALID EXPRESSION: %s'
    },

]
