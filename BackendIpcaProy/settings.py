"""
Django settings for BackendIpcaProy project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

import pusher
from pusher_push_notifications import PushNotifications

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&eu4_%vpm16+%!ypwww#mnkag+18r+g0%bh-ats37&ntf&h&x9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',

    'webpush',
    'django_cleanup',
    'corsheaders',
    'rest_framework',
    'django_filters',
    # 'storages',
    # 'graphene_django',
    # 'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
    # "graphql_auth",

]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost:4500',
]  # If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`
CORS_ORIGIN_REGEX_WHITELIST = [
    'http://localhost:4500',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'django.middleware.gzip.GZipMiddleware',
]

ROOT_URLCONF = 'BackendIpcaProy.urls'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
        # Any other renders
    ),

    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        # Any other parsers
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'BackendIpcaProy.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
''''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd94cksamm1577k',
        'USER': 'bzahbhebawaydf',
        'PASSWORD': '368bbad509c973c58f8b9996b9f7d966f8218c012e324da1c53adcc4307ac7f9',
        'HOST': 'ec2-34-232-212-164.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd9dg60khn12n51',
        'USER': 'oufpqjtxjbikam',
        'PASSWORD': '74939546b162e4f9a33ca5e4be925180f12422287436cd73009a3fb8345eef22',
        'HOST': 'ec2-52-207-124-89.compute-1.amazonaws.com',
        'PORT': '5432',
    },
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'StrawBerryPyDev',
        'USER': 'strawBerryPyDev',
        'PASSWORD': 'strawberrypy',
        'HOST': '204.2.63.19',
        'PORT': '15360',
    },
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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
# AUTH_USER_MODEL = 'core.Usuario'


AUTH_USER_MODEL = 'core.Usuario'

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BH2Qfo0zQTXbPIa6ImMTv2kNfFdbgq2gPPDUdG-olPis4Z4cU3rYNrBcdeogszrUtxTQei1ozUVGvPVD5xDC64Y",
    "VAPID_PRIVATE_KEY": "KIqDC4VngQ1Ns95MQKrAcWVjlTd8JmOoO84giOHajYw",
    "VAPID_ADMIN_EMAIL": "alejocoraizaca@gmail.com"
}
