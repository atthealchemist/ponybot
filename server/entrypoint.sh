#!/bin/bash

setup_server() {
    echo "Making migrations"
    python manage.py makemigrations --no-input
    echo "Migrating"
    python manage.py migrate --no-input
    echo "Saving static for nginx"
    python manage.py collectstatic --no-input
    echo "Creating superuser"
    python manage.py createsuperuser --no-input
}

run_server() {
    # echo "Waiting for db and starting server"
    # ./wait-for-it.sh db:5432
    setup_server

    echo "Running gunicorn"
    gunicorn server.asgi:application --workers=4 -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker --reload
}

run_bot() {
    setup_server
    
    echo "Running bot"
    python manage.py start_bot
}

run_celery() {
    echo "Serving background tasks"
    celery -A server worker -l info
}

run_celery_beat() {
    celery -A server beat -l info
}
 
main() {
    export $(grep -v '^#' .env | xargs)

    if [[ "$#" -eq 0 ]]; then
        exec "/bin/bash"
    fi
 
    case "$1" in
        'server')
            run_server
            ;;
        'bot')
            run_bot
            ;;
        'celery')
            run_celery
            ;;
        'celery-beat')
            run_celery_beat
            ;;
        *)
            exec "$@"
            ;;
    esac
}
 
main "$@"
