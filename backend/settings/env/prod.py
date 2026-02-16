from settings.base import * 

DEBUG=False

ALLOWED_HOSTS=[ "localhost"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
}