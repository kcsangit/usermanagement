#!/bin/sh

echo "Running migrations..."
python manage.py migrate

echo "Collecting static..."
python manage.py collectstatic --noinput

echo "Starting server..."
gunicorn user_management.wsgi:application --bind 0.0.0.0:8000

