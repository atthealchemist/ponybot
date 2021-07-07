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
        user_id = event.object.message.get('from_id')
        peer_id = event.object.message.get('peer_id')
        self.notifier(peer_id,
                      _(f"""
                      Ваш ID (user_id/from_id): {user_id}
                      ID группы (group_id): {event.group_id}
                      ID чата/беседы (peer_id): {peer_id}
                      """))

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()
