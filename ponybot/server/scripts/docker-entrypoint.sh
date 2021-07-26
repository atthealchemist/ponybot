#!/bin/bash
echo "=== STARTING SERVICE $(PONYBOT_SERVER_SERVICE_NAME) ==="
poetry run python manage.py showmigrations | grep '\[ \]'

if [ $? -eq 0 ]; then
 echo "No migrations found, applying..."
 exec poetry run python manage.py migrate
else
    echo "Check migrations: ok!"
fi

echo "Running gunicorn"
exec gunicorn --workers=4 -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker ponybot.asgi