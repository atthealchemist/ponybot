from pony.models import Pony
from django.utils.translation import gettext as _
from vk_api.bot_longpoll import VkBotEventType

from .base import DialogAction


class ActionNamePony(DialogAction):

    def __init__(self, notifier=None, long_poll=None):
        self.notifier = notifier
        self.long_poll = long_poll
        self.aliases = [
            'дать пони имя',
            'назвать пони'
        ]

    def call(self, event):
        user_id = event.object.message.get('from_id')
        peer_id = event.object.message.get('peer_id')

        new_pony_name = self.ask(peer_id, _(
            "Как вы хотите назвать вашу пони?"))

        my_pony = Pony.objects.filter(
            owner=user_id, conversation=peer_id, is_alive=True)
        if not my_pony.exists():
            return
        my_pony = my_pony.first()
        my_pony.set_name(new_name=new_pony_name)
        self.notifier(
            peer_id,
            _(f"Вашу пони теперь зовут {new_pony_name}!")
        )

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()
