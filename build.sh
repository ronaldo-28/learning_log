#!/bin/bash
set -e

echo "🚀 Starting Django Build..."

echo "📦 Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
echo "✅ Dependencies installed."

echo "✨ Collecting static files..."
python3 manage.py collectstatic --noinput --clear
echo "✅ Static files collected."

echo "🗄️ Applying database migrations..."
python3 manage.py migrate --noinput
echo "✅ Migrations applied."

echo "🎉 Build script finished."