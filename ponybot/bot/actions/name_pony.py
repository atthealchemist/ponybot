from pony.models import Pony
from django.utils.translation import gettext as _
from vk_api.bot_longpoll import VkBotEventType

from .base import Action


class ActionNamePony(Action):

    def __init__(self, notifier=None, long_poll=None):
        self.notifier = notifier
        self.long_poll = long_poll
        self.aliases = [
            'дать пони имя',
            'назвать пони'
        ]

    def call(self, event):
        user_id = event.object.message.get('peer_id')
        self.notifier(user_id, _("Как вы хотите назвать вашу пони?"))
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.object.message.get('text')
                my_pony = Pony.objects.filter(owner=user_id)
                if not my_pony.exists():
                    return
                my_pony = my_pony.first()
                my_pony.set_name(new_name=message)
                self.notifier(
                    user_id,
                    _(f"Вашу пони теперь зовут {message}")
                )
                break

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()
