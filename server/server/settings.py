"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

from configurations import Configuration, values

class Dev(Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'y2$jb8^g@zez)&gi$#=t^5d0q73wom$v%3^6e8#1p(yj)qmhs5'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = ['*']


    # Application definition

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
        'django_celery_beat',
        # User-defined apps
        'core',
        'bot'
    ]

    # Constance Config
    CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

    CONSTANCE_CONFIG = {
        'PONY_SELF_EDUCATION_MINS': (30, 'Pony self education period (in mins)', int),
        'PONY_HUNGER_MINS': (30, 'Pony hunger period (in mins)', int),
        'PONY_LEARNING_TIMEOUT_MINS': (5, 'Pony learning timeout (in mins)', int),
        'PONY_FEEDING_TIMEOUT_MINS': (7, 'Pony feeding timeout (in mins)', int),
        'PONY_BOT_ADMINS_LIST': ("", "Ponybot admins user_id list, separated by comma", str),
        'PONY_ICON_LEARNING': ('📚', "Symbol for pony learning", str),
        'PONY_ICON_FEEDING': ('🍼', "Symbol for pony feeding", str),
        'PONY_ICON_NAME': ('🐎', "Symbol for pony name", str),
        'PONY_ICON_RACE': ('👬', "Symbol for pony race", str),
        'PONY_ICON_SATIETY': ('🍎', "Symbol for pony satiety", str),
        'PONY_ICON_LEVEL': ('📖', "Symbol for pony level", str),
        'PONY_ICON_OWNER': ('👥', "Symbol for pony owner", str),
        'PONY_ICON_CONVERSATION': ('💬', "Symbol for pony conversation", str),
    }

    CONSTANCE_CONFIG_FIELDSETS = {
        'General': (
            'PONY_BOT_ADMINS_LIST',
        ),
        'Periods/Timeouts': (
            'PONY_SELF_EDUCATION_MINS',
            'PONY_HUNGER_MINS',
            'PONY_LEARNING_TIMEOUT_MINS',
            'PONY_FEEDING_TIMEOUT_MINS'
        ),
        'Icons': (
            'PONY_ICON_LEARNING',
            'PONY_ICON_FEEDING',
            'PONY_ICON_NAME',
            'PONY_ICON_RACE',
            'PONY_ICON_SATIETY',
            'PONY_ICON_LEVEL',
            'PONY_ICON_OWNER',
            'PONY_ICON_CONVERSATION',
        ),
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

    ROOT_URLCONF = 'server.urls'

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

    WSGI_APPLICATION = 'server.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/3.1/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': os.environ.get('DJANGO_DB_HOST'),
            'PORT': os.environ.get('DJANGO_DB_PORT'),
            'NAME': os.environ.get('DJANGO_DB_NAME'),
            'USER': os.environ.get('DJANGO_DB_USER'),
            'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD'),
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
    STATIC_ROOT = BASE_DIR / 'static'

    AUTH_USER_MODEL = 'core.PonybotUser'

    # Env settings
    VK_API_TOKEN = values.Value()
    VK_GROUP_ID = values.Value()
    
    # Celery Settings
    CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
    CELERY_BROKER_URL = values.Value()