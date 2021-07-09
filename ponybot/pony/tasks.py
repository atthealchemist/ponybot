from celery import shared_task
from .models import Pony

from datetime import timedelta
from django.utils import timezone
from django.db.models import F

from constance import config
from ponybot.celery import app

from pony.exceptions import PonyOverfeedException, PonyTiredException


@app.task
def teach_ponies():
    # print("Teaching ponies")
    for pony in Pony.objects.filter(
        last_learning__lt=timezone.now() + timedelta(seconds=config.PONY_SELF_EDUCATION_MINS),
        is_alive=True
    ):
        try:
            exp_points = pony.learn()
            print(f"{pony} has learned something new! experience += {exp_points}")
        except PonyTiredException:
            continue


@app.task
def hunger_ponies():
    from bot.notifier import VkNotifier
    notifier = VkNotifier()
    # print("Hunger ponies")
    for pony in Pony.objects.filter(
        last_feeding__gte=F('last_feeding') +
        timedelta(seconds=config.PONY_HUNGER_MINS),
        is_alive=True
    ):
        try:
            notifier.notify(pony.owner,
                            f"Ваша пони голодает! Её сытость равна {pony.satiety}. Пожалуйста, покормите её!")
            print(f"{pony} feel hunger: satiety -= 1")
            pony.hunger()
        except PonyOverfeedException:
            continue
