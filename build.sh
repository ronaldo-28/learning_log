#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Building project..."

# Upgrade pip and install requirements
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Build finished."