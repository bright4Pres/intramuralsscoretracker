#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

cd scoretracker

echo "=========================================="
echo "About to run collectstatic..."
echo "=========================================="
python manage.py collectstatic --no-input

echo "=========================================="
echo "About to run migrations..."
echo "=========================================="
python manage.py migrate --verbosity 2

echo "=========================================="
echo "About to initialize teams..."
echo "=========================================="
python manage.py init_teams

echo "=========================================="
echo "About to initialize games..."
echo "=========================================="
python manage.py init_games

# Create superuser if it doesn't exist
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    echo "=========================================="
    echo "About to create superuser..."
    echo "=========================================="
    python manage.py createsuperuser --noinput || echo "Superuser already exists"
fi

echo "=========================================="
echo "Build script completed successfully!"
echo "=========================================="
