#!/bin/bash
set -e

echo "🚀 Starting Django Build..."

echo "📦 Installing dependencies..."
pip install uv
uv sync
echo "✅ Dependencies installed."

echo "✨ Collecting static files..."
uv run python manage.py collectstatic --noinput --clear
echo "✅ Static files collected."

echo "🗄️ Applying database migrations..."
uv run python manage.py migrate --noinput
echo "✅ Migrations applied."

echo "🎉 Build script finished."