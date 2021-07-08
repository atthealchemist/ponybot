from celery import shared_task
from .models import Pony

from datetime import timedelta, timezone

from constance import config


@shared_task
def teach_ponies():
    for pony in Pony.objects.filter(
        last_learning__lte=timezone.now() - timedelta(minutes=config.PONY_SELF_EDUCATION_MINS),
        is_alive=True
    ):
        exp_points = pony.learn()
        print(f"{pony} has learned something new! experience += {exp_points}")


@shared_task
def hunger_ponies():
    for pony in Pony.objects.filter(
        last_feeding__lte=timezone.now() - timedelta(minutes=config.PONY_HUNGER_MINS),
        is_alive=True
    ):
        print(f"{pony} feel hunger: satiety -= 1")
        pony.hunger()
