import dj_database_url

from .base import *

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

# WhiteNoise inserted directly after SecurityMiddleware
_security_idx = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')
MIDDLEWARE.insert(_security_idx + 1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STORAGES = {
    # Media files → Cloudflare R2 (S3-compatible)
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        'OPTIONS': {
            'bucket_name': os.environ.get('CLOUDFLARE_R2_BUCKET_NAME'),
            'endpoint_url': os.environ.get('CLOUDFLARE_R2_ENDPOINT_URL'),
            'access_key': os.environ.get('CLOUDFLARE_R2_ACCESS_KEY_ID'),
            'secret_key': os.environ.get('CLOUDFLARE_R2_SECRET_ACCESS_KEY'),
            'location': os.environ.get('CLOUDFLARE_R2_MEDIA_PREFIX', 'prod'),
            'file_overwrite': False,
            'default_acl': 'public-read',
        },
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
