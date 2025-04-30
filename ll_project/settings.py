# ll_project/settings.py

import os # Add this import
from platformshconfig import Config # Keep if you still use Platform.sh sometimes, otherwise remove
from pathlib import Path
import dj_database_url # Add this import

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Read SECRET_KEY from environment variable
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    # Use a default value only for local development if needed,
    # but prefer setting it in your local env too.
    # Ensure the deployed app ALWAYS has DJANGO_SECRET_KEY set.
    'django-insecure-mibxt7sboxg%r)9t6z=a6@weyo(thgbknfcwgyowgx9$5s4&=!'
)

# SECURITY WARNING: don't run with debug turned on in production!
# Set DEBUG based on environment variable, default to False for safety
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

# Configure ALLOWED_HOSTS for Vercel
ALLOWED_HOSTS = []
VERCEL_URL = os.environ.get('VERCEL_URL')
if VERCEL_URL:
    # Vercel provides the URL of the deployment
    # Allow the primary Vercel domain and potentially custom domains
    ALLOWED_HOSTS.append(VERCEL_URL.replace('https://', ''))
    # Add any custom domains linked in Vercel here, e.g.:
    # ALLOWED_HOSTS.append('www.yourdomain.com')
else:
    # For local development
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    # My apps.
    'learning_logs',
    'accounts',

    # Third party apps.
    'django_bootstrap5',

    # Default django apps.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Add whitenoise here
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Add whitenoise middleware HERE
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

# Default to SQLite for local development if DATABASE_URL is not set
# Vercel will set the DATABASE_URL environment variable when linked
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600, # Optional: connection pooling
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}" # Fallback to SQLite locally
    )
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# Keep AUTH_PASSWORD_VALIDATORS as is

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
# Keep LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ as is

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = 'static/'
# Define where collectstatic will gather files
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Tell WhiteNoise where to find files and enable compression/caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/dev/ref/settings/#default-auto-field
# Keep DEFAULT_AUTO_FIELD as is

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# My settings.
# Keep LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL, LOGIN_URL as is

LOGIN_REDIRECT_URL = 'learning_logs:index'
LOGOUT_REDIRECT_URL = 'learning_logs:index'
LOGIN_URL = 'accounts:login'


# --- Remove or comment out the Platform.sh specific section ---
# # Platform.sh settings.
# config = Config()
# if config.is_valid_platform():
#     ALLOWED_HOSTS.append('.platformsh.site')
#     DEBUG = False

#     if config.appDir:
#         # Note: STATIC_ROOT is now handled above
#         pass #STATIC_ROOT = Path(config.appDir) / 'static'
#     if config.projectEntropy:
#         # Note: SECRET_KEY is now handled by env var
#         pass #SECRET_KEY = config.projectEntropy

#     if not config.in_build():
#         db_settings = config.credentials('database')
#         # Note: DATABASES is now handled by dj-database-url
#         pass # DATABASES = { ... }
# --- End of Platform.sh section ---


# Vercel specific settings (optional but good practice)
CSRF_TRUSTED_ORIGINS = []
if VERCEL_URL:
    CSRF_TRUSTED_ORIGINS.append(f'https://{VERCEL_URL.replace("https://", "")}')
    # Add custom domains here too if needed
    # CSRF_TRUSTED_ORIGINS.append('https://www.yourdomain.com')

# Use secure cookies in production
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True # Redirect HTTP to HTTPS
    # Optional: HSTS settings
    # SECURE_HSTS_SECONDS = 31536000 # 1 year
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True