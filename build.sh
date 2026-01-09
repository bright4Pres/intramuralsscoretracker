#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

cd scoretracker
python manage.py collectstatic --no-input
python manage.py migrate --run-syncdb
python manage.py init_teams
python manage.py init_games

# Create superuser if it doesn't exist
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    python manage.py createsuperuser --noinput || echo "Superuser already exists"
fi
