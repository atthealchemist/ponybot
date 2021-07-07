from .base import Action
from django.utils.translation import gettext as _


class ActionGetId(Action):

    def __init__(self, notifier=None):
        self.notifier = notifier
        self.aliases = [
            'мой ид',
            'мой id'
        ]

    def call(self, event):
        user_id = event.object.message.get('peer_id')
        self.notifier(user_id,
                      _(f"Ваш ID: {event.object.get('message').get('from_id')}\nID группы: {event.group_id}"))

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()
