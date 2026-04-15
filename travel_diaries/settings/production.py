import dj_database_url

from .base import *

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [h for h in os.environ.get('ALLOWED_HOSTS', '').split(',') if h]

CSRF_TRUSTED_ORIGINS = [h for h in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if h]

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

# WhiteNoise inserted directly after SecurityMiddleware
_security_idx = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')
MIDDLEWARE.insert(_security_idx + 1, 'whitenoise.middleware.WhiteNoiseMiddleware')

MEDIA_ROOT = '/var/data/media'

STORAGES = {
    # Media files → local filesystem (Render persistent disk at /var/data/media)
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    # Static files → WhiteNoise with Brotli/gzip compression + cache manifests
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# Security headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
