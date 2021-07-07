from math import e
from pony.exceptions import PonyOverfeedException
from bot.actions.create_pony import ActionCreatePony
from django.utils.translation import gettext as _

from pony.models import Pony

from .base import SimpleAction


class ActionFeedPony(SimpleAction):

    def __init__(self, notifier=None):
        super().__init__(notifier)

        self.aliases = [
            'кормить пони',
            'покормить пони'
        ]

    def call(self, event):
        user_id = event.object.message.get('peer_id')

        user_ponies = Pony.objects.filter(owner=user_id)
        if not user_ponies.exists():
            self.notifier(user_id, _(
                f"У вас ещё нет ни одной пони!\nЗаведите её, написав одну из следующих команд: {str(ActionCreatePony())}"
            ))
            return
        user_pony = user_ponies.first()
        try:
            user_pony.feed()
            self.notifier(user_id, _(
                f"Ваша пони покушала и теперь её сытость равна {user_pony.satiety}"))
        except PonyOverfeedException as ex:
            self.notifier(user_id, _(str(ex)))
