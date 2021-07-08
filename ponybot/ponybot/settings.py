"""
Django settings for ponybot project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import sys

from configurations import Configuration, values
from pathlib import Path


class BaseConfiguration(Configuration):
    BASE_DIR = Path(__file__).resolve().parent.parent
    DOTENV = BASE_DIR / '.env'

    # Application definition
    SECRET_KEY = values.Value()

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Third-party apps
        'constance',
        'constance.backends.database',
        'rest_framework',
        'django_celery_beat',
        # User defined apps
        'pony',
        'bot'
    ]

    # Constance Config
    CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

    CONSTANCE_CONFIG = {
        'PONY_LEARNING_TIMEOUT_MINS': (5, 'Pony learning timeout (in mins)', int),
        'PONY_FEEDING_TIMEOUT_MINS': (7, 'Pony feeding timeout (in mins)', int)
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': '[%(asctime)s] [%(name)s - %(levelname)s] %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'console',
            },
        },
        'loggers': {
            'Ponybot': {
                'level': 'DEBUG',
                'handlers': ['console'],
            },
        },
    }

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'ponybot.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
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

    STATIC_URL = '/static/'


class Dev(BaseConfiguration):
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    ALLOWED_HOSTS = ['*']

    # Application definition
    # SECRET_KEY = values.Value()
    VK_API_TOKEN = values.Value()
    VK_GROUP_ID = values.Value()

    # DRF Settings
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10
    }

    # Celery Beat Schedule
    CELERY_BEAT_SCHEDULE = {
        "scheduled_task__teach_ponies": {
            "task": "pony.tasks.teach_ponies",
            "schedule": 1.0,
            "args": ()
        },
        "scheduled_task__hunger_ponies": {
            "task": "pony.tasks.hunger_ponies",
            "schedule": 1.0,
            "args": ()
        },
    }


class Production(BaseConfiguration):
    DEBUG = False
    ALLOWED_HOSTS = [
        '127.0.0.1'
    ]
