# dental/settings/base.py
# dental is projectdirectory. heet ook vaak src

from dotenv import load_dotenv

from pathlib import Path
import os

# Setting to deploy to heroku
import django_heroku
import dj_database_url
from decouple import config

# import rest_framework

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

load_dotenv( BASE_DIR / '.env', )

# set PROJ_DIR = 'C:\OSGeo4W\'

# Application definition

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  # my apps
  #'djgeojson',
  #'django.contrib.gis',
  'users.apps.UsersConfig',
  'website',
  'stocks.apps.StocksConfig',
  'theblog',
  'events',
  'maps.apps.MapsConfig',
  'energie',
  'csvs.apps.CsvsConfig',
  'sales.apps.SalesConfig',
  'measurements.apps.MeasurementsConfig',
  'photos.apps.PhotosConfig',
  'meetups.apps.MeetupsConfig',
  'portfolio.apps.PortfolioConfig',
  'store.apps.StoreConfig',
  'datalab.apps.DatalabConfig',
  'rakken.apps.RakkenConfig',
  # support
  'crispy_forms',
  'import_export',
  'ckeditor',
  #'ckeditor_uploader',
  'rest_framework',
  'rest_framework.authtoken',
  'drf_spectacular',
  'django_filters',
  'django_extensions',
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'dental.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'dental.context_processors.project_context'
        # 'app_name.module_name.function_name'
      ],
    },
  },
]

WSGI_APPLICATION = 'dental.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
  {
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  },
]

CKEDITOR_ALLOW_NONIMAGE_FILES = False

CRISPY_TEMPLATE_PACK = 'bootstrap4'

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework.authentication.SessionAuthentication',
  ],
  'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N  = True
USE_L10N  = True
USE_TZ    = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_DIRS = [
  BASE_DIR / 'static',
  BASE_DIR / 'media',
]    # Django zoekt altijd in de static-folder van de app, maar daarnaast ook op deze lokatie(s)

STATIC_URL       = '/static/'                # URL via welke staticfiles toegankelijk zijn van buiten de app
STATIC_ROOT      = BASE_DIR / 'staticfiles' # absoluut pad waar project staticfiles worden opgeslagen door collectstatic

MEDIA_URL        = '/media/'                # URL via welke mediafiles toegankelijk zijn van buiten de app
MEDIA_ROOT       = BASE_DIR / 'mediafiles' # absoluut pad waar project mediafiles worden opgeslagen
#MEDIAFILES_DIRS  = [BASE_DIR / 'media',]    # Django zoekt altijd in de media-folder van de app, maar daarnaast ook op deze lokatie(s)


LOGIN_URL  = 'login'
LOGIN_REDIRECT_URL  = 'index'
LOGOUT_REDIRECT_URL = 'index'

BASE_COUNTRY = "NL"

# Session time (seconds) default is 2 weeks
# SESSION_COOKIE_AGE = 120

# Setting for deploying to heroku
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'dental.storage.WhiteNoiseStaticFilesStorage'

# email settings using gmail as mailserver
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_HOST_USER     = 'cfidevelopt'
EMAIL_HOST_PASSWORD = os.getenv('GMAILPW')
EMAIL_USE_TLS       = True
EMAIL_USE_SSL       = False
'''
# email settings using localhost as mailserver
# start mailserver: python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
'''

django_heroku.settings(locals())

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'