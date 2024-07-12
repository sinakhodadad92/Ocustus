#!/bin/sh


python manage.py flush --no-input
python manage.py makemigrations inspector
python manage.py migrate

exec "$@"