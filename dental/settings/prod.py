# dental/settings/production.py

import os

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = True
ALLOWED_HOSTS = ['*', 'localhost', 'oefendjango.herokuapp.com']
#LOGGING = [...]

WHITENOISE_MANIFEST_STRICT = False