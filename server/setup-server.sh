#!/bin/bash

echo "Making migrations"
python manage.py makemigrations --no-input
echo "Migrating"
python manage.py migrate --no-input
echo "Saving static for nginx"
python manage.py collectstatic --no-input
echo "Creating superuser"
python manage.py createsuperuser --no-input