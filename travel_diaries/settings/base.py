import base64
import os
from pathlib import Path

import logfire
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

encoded_key = os.environ.get("SECRET_KEY")
if encoded_key:
    SECRET_KEY = base64.b64decode(encoded_key).decode('utf-8')
else:
    raise Exception("SECRET_KEY environment variable not set.")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'tailwind',
    'theme',
    'blog',
    'map',
]

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ['127.0.0.1']

BLOG_TAGLINE = 'AI · Community · Human things'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'travel_diaries.middleware.PageLoadTimeMiddleware',
]

ROOT_URLCONF = 'travel_diaries.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'travel_diaries.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-uk'
TIME_ZONE = 'Europe/Dublin'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'logfire': {
            'class': 'logfire.LogfireLoggingHandler',
        },
    },
    'root': {
        'handlers': ['logfire'],
    },
}

# Logfire — environment is set per-service via the ENVIRONMENT env var
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'prod')

api_key = os.environ.get('LOGFIRE_TOKEN')
if api_key:
    logfire.configure(
        token=api_key,
        service_name='django-travel-diary',
        environment=ENVIRONMENT,
    )
    logfire.instrument_system_metrics({
        'process.cpu.utilization': None,
        'system.cpu.simple_utilization': None,
        'system.memory.usage': ['available', 'used'],
        'system.memory.utilization': ['available', 'used'],
        'system.swap.utilization': ['used'],
        'system.network.io': ['transmit', 'receive'],
    })
    logfire.instrument_django()
    logfire.instrument_psycopg()
