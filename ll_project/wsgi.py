import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'll_project.settings')

django.setup()

from django.core.management import call_command

try:
    call_command('migrate', '--noinput')
except Exception as e:
    print(f"Migration error: {e}")

# Fix the Sites framework record
try:
    from django.contrib.sites.models import Site
    Site.objects.update_or_create(
        id=1,
        defaults={
            'domain': 'learning-log8.vercel.app',
            'name': 'Learning Log'
        }
    )
    print("Site record OK")
except Exception as e:
    print(f"Site fix error: {e}")

application = get_wsgi_application()
app = application