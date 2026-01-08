#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python scoretracker/manage.py collectstatic --no-input
python scoretracker/manage.py migrate
