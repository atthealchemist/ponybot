from .models import Pony

from constance import config

from datetime import timedelta
from django.utils import timezone

from core.celery import app, api


@app.task
def teach_ponies():
    for pony in Pony.objects.filter(is_alive=True):
        estimated_educated_time = pony.last_learning + timedelta(minutes=config.PONY_SELF_EDUCATION_MINS)
        now = timezone.now()
        if now >= estimated_educated_time:
            exp_points = pony.learn()
            api.notify(
                pony, 
                f"{pony.name} выучила что-то новенькое! "
                f"Опыт увеличился на {exp_points} и стал равен {pony.experience}.",
                mention=True
            )


@app.task
def starvy_ponies():
    for pony in Pony.objects.filter(is_alive=True):
        # Пони начинает голодать через определённый период:
        # Например, через 30 секунд после предыдущей покормки
        # То есть, если сейчас больше, чем 3 минут после последнего корма -
        # Пони голодает. При этом периодичность её голодания - 3600 секунд (1 час, например).
        estimated_hunger_time = pony.last_feeding + timedelta(minutes=config.PONY_HUNGER_MINS)
        now = timezone.now()
        # Пони покормили в 9:30. Через полчаса она проголодается.
        # Следовательно, если её не покормили в 10 часов, то она начинает голодать
        if now >= estimated_hunger_time:
            pony.hunger()
            api.notify(
                pony, 
                f"{pony.name} голодает! "
                f"Сытость уменьшилась на 1 и теперь равна {pony.satiety}! " 
                "Покормите её, или она умрёт!",
                mention=True
            )
