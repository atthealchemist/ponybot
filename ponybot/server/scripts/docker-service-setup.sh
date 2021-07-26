#!/bin/bash

echo "=== SETTING UP SERVICE $(PONYBOT_SERVER_SERVICE_NAME) ==="

# Migrate database
python manage.py migrate
# Creating superuser
python manage.py createsuperuser
# Collecting static files
python manage.py collectstatic

echo "=== FINISHED ==="