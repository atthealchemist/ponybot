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
            'покормить пони',
            'покормить',
            'покушать'
        ]

    def call(self, event):
        user_id = event.object.message.get('from_id')
        peer_id = event.object.message.get('peer_id')

        user_ponies = Pony.objects.filter(
            owner=user_id,
            # conversation=peer_id,
            is_alive=True
        )
        if not user_ponies.exists():
            self.warn(peer_id, _(
                f"У вас ещё нет ни одной пони!\nЗаведите её, написав одну из следующих команд: {str(ActionCreatePony())}"
            ))
            return
        user_pony = user_ponies.first()
        try:
            user_pony.feed()
            self.say(peer_id, _(
                f"Ваша пони ({user_pony.name}) покушала и теперь её сытость равна {user_pony.satiety}"))
        except PonyOverfeedException as ex:
            self.warn(peer_id, _(str(ex)))
