SECRET_KEY = 'not a secret key'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'trees',
    }
}
