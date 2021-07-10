import configurations
import os
from celery import Celery



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ponybot.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')


configurations.setup()

app = Celery('ponybot', broker="pyamqp://guest@localhost//")
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "scheduled_task__teach_ponies": {
        "task": "pony.tasks.teach_ponies",
        # We call that task every second cause we're stuck to last_learning timestamp and check it
        "schedule": 1.0,
        "args": ()
    },
    "scheduled_task__hunger_ponies": {
        "task": "pony.tasks.hunger_ponies",
        "schedule": 1.0,
        "args": ()
    },
}
