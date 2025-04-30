#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "BUILD SCRIPT STARTING..." # Added for clear log indication

# Upgrade pip and install requirements
echo "Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo "Dependencies installed."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
echo "Static files collected."

# Apply database migrations (CRITICAL STEP)
echo "Applying database migrations..."
python manage.py migrate --noinput
echo "Database migrations applied."

echo "BUILD SCRIPT FINISHED."