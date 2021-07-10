from .models import Pony

from datetime import timedelta
from django.db.models import F

from ponybot.celery import app


@app.task
def teach_ponies():
    for pony in Pony.objects.filter(
        last_feeding__gte=F('last_learning') + timedelta(seconds=30),
        is_alive=True
    ):
        exp_points = pony.learn()
        print(f"{pony} has learned something new! experience += {exp_points}")


@app.task
def starvy_ponies():
    for pony in Pony.objects.filter(
        last_feeding__gte=F('last_feeding') +
        timedelta(seconds=30),
        is_alive=True
    ):
        print(f"{pony} feel hunger: satiety -= 1")
        pony.hunger()
