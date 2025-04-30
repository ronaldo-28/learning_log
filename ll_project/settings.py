# ll_project/settings.py

# ... other imports ...
import os
from pathlib import Path
import dj_database_url

# ... SECRET_KEY, DEBUG ...

# Configure ALLOWED_HOSTS for Vercel
ALLOWED_HOSTS = []
VERCEL_URL = os.environ.get('VERCEL_URL') # Specific deployment URL (e.g., project-hash-user.vercel.app)

if VERCEL_URL:
    # Add the specific Vercel deployment URL (without https://)
    # Remove potential trailing slashes just in case
    ALLOWED_HOSTS.append(VERCEL_URL.replace('https://', '').rstrip('/'))

# Add the generic wildcard for Vercel preview/branch URLs AND the main .vercel.app domain
# This covers learning-log-cyan.vercel.app and any preview URLs like project-git-branch-user.vercel.app
# Ensure this is added *after* the specific URL if it exists
ALLOWED_HOSTS.append('.vercel.app')

# Add any custom domains manually if needed
# Example:
# CUSTOM_DOMAIN = os.environ.get('CUSTOM_DOMAIN')
# if CUSTOM_DOMAIN:
#     ALLOWED_HOSTS.append(CUSTOM_DOMAIN)


if not ALLOWED_HOSTS or os.environ.get('DJANGO_DEBUG') == 'True':
    # Fallback for local development or if Vercel vars aren't set somehow
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])

# Ensure no duplicates (optional, but clean)
ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))


# ... rest of INSTALLED_APPS, MIDDLEWARE, TEMPLATES, WSGI_APPLICATION, DATABASES ...

# --- Update CSRF_TRUSTED_ORIGINS as well for consistency ---

# Vercel specific settings (optional but good practice)
CSRF_TRUSTED_ORIGINS = []
if VERCEL_URL:
    # Trust the specific deployment URL
    CSRF_TRUSTED_ORIGINS.append(f'https://{VERCEL_URL.replace("https://", "").rstrip("/")}')

# Also trust the production domain and preview domains via the wildcard pattern
# Note: CSRF_TRUSTED_ORIGINS needs the scheme (https://)
CSRF_TRUSTED_ORIGINS.append('https://*.vercel.app')

# Add custom domains if needed (ensure https)
# Example:
# if CUSTOM_DOMAIN:
#      CSRF_TRUSTED_ORIGINS.append(f'https://{CUSTOM_DOMAIN}')

# Remove duplicates if any
CSRF_TRUSTED_ORIGINS = list(set(CSRF_TRUSTED_ORIGINS))

# --- End CSRF Update ---

# Use secure cookies in production
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True # Usually safe on Vercel as it handles TLS termination
    # SECURE_HSTS_SECONDS = 31536000 # Optional HSTS
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True

# ... rest of the file ...