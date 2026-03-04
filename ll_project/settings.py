# ll_project/settings.py

import os
from pathlib import Path
import dj_database_url
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-mibxt7sboxg%r)9t6z=a6@weyo(thgbknfcwgyowgx9$5s4&=!'
)

DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = []
VERCEL_URL = os.environ.get('VERCEL_URL')

if VERCEL_URL:
    ALLOWED_HOSTS.append(VERCEL_URL.replace('https://', '').rstrip('/'))

ALLOWED_HOSTS.append('.vercel.app')

if not ALLOWED_HOSTS or DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])

ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))

SITE_ID = 1

INSTALLED_APPS = [
    # My apps
    'learning_logs',
    'accounts',

    # Third party
    'django_bootstrap5',

    # Allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Default Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ROOT_URLCONF = 'll_project.urls'

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

WSGI_APPLICATION = 'll_project.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        ssl_require=os.environ.get('DJANGO_DB_SSL_REQUIRE', 'False') == 'True',
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth redirects
LOGIN_REDIRECT_URL = 'learning_logs:index'
LOGOUT_REDIRECT_URL = 'learning_logs:index'
LOGIN_URL = 'accounts:login'

# Allauth settings
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID', ''),
            'secret': os.environ.get('GOOGLE_CLIENT_SECRET', ''),
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
    }
}

# Email — reads from .env locally, from Vercel env vars in production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER', '')

# Vercel CSRF
CSRF_TRUSTED_ORIGINS = []
if VERCEL_URL:
    CSRF_TRUSTED_ORIGINS.append(f'https://{VERCEL_URL.replace("https://", "").rstrip("/")}')
CSRF_TRUSTED_ORIGINS.append('https://*.vercel.app')
CSRF_TRUSTED_ORIGINS = list(set(CSRF_TRUSTED_ORIGINS))

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
    message_constants.DEBUG:   'secondary',
    message_constants.INFO:    'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR:   'danger',
}