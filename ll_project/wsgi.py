import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'll_project.settings')

# Run collectstatic and migrate on cold start
django.setup()

from django.core.management import call_command
try:
    call_command('migrate', '--noinput')
except Exception as e:
    print(f"Migration error: {e}")

application = get_wsgi_application()
app = application