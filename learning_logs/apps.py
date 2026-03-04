from django.apps import AppConfig

class LearningLogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'learning_logs'

    def ready(self):
        # Auto-fix the missing Site ID for Vercel and django-allauth
        try:
            from django.contrib.sites.models import Site
            Site.objects.get_or_create(
                id=1, 
                defaults={'domain': 'learning-log8.vercel.app', 'name': 'Learning Log'}
            )
        except Exception:
            # Ignore errors if the database hasn't migrated yet
            pass