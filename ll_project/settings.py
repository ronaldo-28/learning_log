# ll_project/settings.py

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-mibxt7sboxg%r)9t6z=a6@weyo(thgbknfcwgyowgx9$5s4&=!' # Default for local only
)

# SECURITY WARNING: don't run with debug turned on in production!
# DEFINE DEBUG HERE:
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

# Configure ALLOWED_HOSTS for Vercel (Uses VERCEL_URL, which is fine to define later if needed)
ALLOWED_HOSTS = []
VERCEL_URL = os.environ.get('VERCEL_URL') # Specific deployment URL

if VERCEL_URL:
    ALLOWED_HOSTS.append(VERCEL_URL.replace('https://', '').rstrip('/'))

ALLOWED_HOSTS.append('.vercel.app') # Add wildcard

# Fallback for local development
if not ALLOWED_HOSTS or DEBUG: # It's okay to use DEBUG here as it's defined above
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])

ALLOWED_HOSTS = list(set(ALLOWED_HOSTS)) # Remove duplicates


# Application definition
INSTALLED_APPS = [
    # ... your apps
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... other middleware
]

ROOT_URLCONF = 'll_project.urls'

TEMPLATES = [
    # ... your template config
]

WSGI_APPLICATION = 'll_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
}


# Password validation
# ... validators


# Internationalization
# ... i18n settings


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# My settings.
LOGIN_REDIRECT_URL = 'learning_logs:index'
LOGOUT_REDIRECT_URL = 'learning_logs:index'
LOGIN_URL = 'accounts:login'


# Vercel specific settings / CSRF
CSRF_TRUSTED_ORIGINS = []
if VERCEL_URL:
    CSRF_TRUSTED_ORIGINS.append(f'https://{VERCEL_URL.replace("https://", "").rstrip("/")}')
CSRF_TRUSTED_ORIGINS.append('https://*.vercel.app')
# Add custom domains if needed
CSRF_TRUSTED_ORIGINS = list(set(CSRF_TRUSTED_ORIGINS))

# Use secure cookies in production
# THIS SECTION MUST COME *AFTER* DEBUG IS DEFINED
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    # SECURE_HSTS_SECONDS = 31536000 # Optional HSTS
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True