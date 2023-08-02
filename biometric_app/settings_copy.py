
from pathlib import Path
import dj_database_url
from decouple import config
import django_heroku
import boto3
import os
from biometric_app.jazzmin_settings import *
from storages.backends.s3boto3 import S3Boto3Storage


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&o+78t$gv4i+@n-7@nx-0f4*n3agi2458__p0p^mdr-_0&uk27'

DEBUG = True
ALLOWED_HOSTS = ["*"]
# Application definition


ADMIN_DASHBOARD_TEMPLATE = "dashboard"


INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend',
    'dashboard',
    'authuser',
    'customstorage',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'authuser.middleware.SetLoggedinUserRoleAsGroup',
]

ROOT_URLCONF = 'biometric_app.urls'

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
                'biometric_app.context.context1.processor'
            ],
        },
    },
]
# specify the new user model for this app
AUTH_USER_MODEL = 'authuser.User'
WSGI_APPLICATION = 'biometric_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


if config('ENVIRONMENT') == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
elif config('ENVIRONMENT') == 'production':
    DATABASES = {
        'default': dj_database_url.config(default='postgres://bkvgivkwwlvgln:e5eda2aa5fce7e77121d4f4b15c58a78b57718796beeec9b8ec28f083840e018@ec2-34-197-91-131.compute-1.amazonaws.com:5432/dac11gg9fa1e4v')
    }
else:
    pass


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


if config('ENVIRONMENT') == 'production':
    AWS_ACCESS_KEY_ID = config('BUCKETEER_AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('BUCKETEER_AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('BUCKETEER_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('BUCKETEER_AWS_REGION')

    DEFAULT_FILE_STORAGE = 'biometric_app.custom_media.S3MediaStorage'

    # Configure static and media URLs for S3
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = 'media'  # Set the S3 bucket subdirectory for media files
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

django_heroku.settings(locals())


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = f"./static/"
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
