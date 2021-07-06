from celery import shared_task
from .models import Pony

from django.db.models import F
from datetime import timedelta


@shared_task
def teach_ponies():
    for pony in Pony.objects.filter(
        last_learning=F('last_learning') + timedelta(seconds=12)
    ):
        exp_points = pony.learn()
        print(f"{pony} has learned something new! experience += {exp_points}")


@shared_task
def hunger_ponies():
    for pony in Pony.objects.filter(
        last_feeding=F('last_feeding') + timedelta(seconds=6)
    ):
        print(f"{pony} feel hunger: satiety -= 1")
        pony.hunger()
