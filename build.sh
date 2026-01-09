#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

cd scoretracker

echo "Starting Django setup..."
echo "DATABASE_URL is: $DATABASE_URL"

python manage.py collectstatic --no-input
echo "Collectstatic completed"

python manage.py migrate
echo "Migration completed"

python manage.py init_teams
echo "Init teams completed"

python manage.py init_games
echo "Init games completed"

# Create superuser if it doesn't exist
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    python manage.py createsuperuser --noinput || echo "Superuser already exists"
fi

echo "Build script completed successfully"
