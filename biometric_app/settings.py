
from pathlib import Path
import dj_database_url
from decouple import config
import django_heroku
import boto3
import os
from biometric_app.jazzmin_settings import *
from storages.backends.s3boto3 import S3Boto3Storage
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&o+78t$gv4i+@n-7@nx-0f4*n3agi2458__p0p^mdr-_0&uk27'

DEBUG = True
ALLOWED_HOSTS = ["*"]
# Application definition

CSRF_TRUSTED_ORIGINS = ['https://eb04-105-113-33-172.ngrok-free.app']

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
    'storages',
    'lecturer_dashboard',
    'student_dashboard',
    'django_celery_beat',
    'periodictask',
    'channels'
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
ASGI_APPLICATION = 'biometric_app.routing.application'

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
        'default': dj_database_url.config(default=config('DATABASE_URL'))
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

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = f"static/"
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# settings.py
# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'


CELERY_BEAT_SCHEDULE = {
    'check_time_interval': {
        'task': 'periodictask.tasks.runtask',
        'schedule': crontab(minute='*/5'),  # Execute the task every 15 minutes
    },

    'check_time_interval': {
            'task': 'periodictask.tasks.check_time_interval', 
            'schedule': crontab(minute='*/3'),  # Execute the task every 15 minutes
        },
    
}