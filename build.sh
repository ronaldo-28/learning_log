#!/bin/bash
set -e

echo "🚀 Starting Django Build..."

# We don't need pip install here because Vercel's @vercel/python builder 
# handles requirements.txt automatically in the background.

echo "✨ Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "🗄️ Applying database migrations..."
python3 manage.py migrate --noinput

echo "✅ Build script finished."