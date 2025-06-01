#!/bin/bash
set -e
echo "BUILD SCRIPT STARTING..."
echo "Installing dependencies..."
python3 -m pip install --upgrade pip # Use python3
python3 -m pip install -r requirements.txt # Use python3
echo "Dependencies installed."
echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear # Use python3
echo "Static files collected."
echo "Applying database migrations..."
python3 manage.py migrate --noinput # Use python3
echo "Database migrations applied."
echo "BUILD SCRIPT FINISHED."