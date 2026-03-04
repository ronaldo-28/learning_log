import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'll_project.settings')

# Setup Django
django.setup()

from django.core.management import call_command
from django.contrib.sites.models import Site  # <-- Imported Site model

try:
    # 1. Run migrations
    call_command('migrate', '--noinput')
    
    # 2. Automatically fix the Site ID 500 error on the live database!
    Site.objects.get_or_create(id=1, defaults={'domain': 'learning-log8.vercel.app', 'name': 'Learning Log'})

except Exception as e:
    print(f"Startup error: {e}")

application = get_wsgi_application()
app = application