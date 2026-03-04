#!/bin/bash
set -e

echo "🚀 Starting Django Build..."

echo "📦 Installing dependencies..."
uv sync
echo "✅ Dependencies installed."

echo "✨ Collecting static files..."
uv run python manage.py collectstatic --noinput --clear
echo "✅ Static files collected."

echo "🗄️ Applying database migrations..."
uv run python manage.py migrate --noinput
echo "✅ Migrations applied."

echo "🌐 Setting up django-allauth Site ID..."
uv run python manage.py shell -c "from django.contrib.sites.models import Site; Site.objects.get_or_create(id=1, defaults={'domain': 'learning-log8.vercel.app', 'name': 'Learning Log'})"
echo "✅ Site ID fixed."

echo "🎉 Build script finished."