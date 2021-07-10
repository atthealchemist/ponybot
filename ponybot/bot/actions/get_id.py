from .base import SimpleAction
from django.utils.translation import gettext as _


class ActionGetId(SimpleAction):

    def __init__(self, notifier=None):
        super().__init__(notifier)

        self.aliases = [
            'мой ид',
            'мой id'
        ]

    def call(self, event):
        user_id = event.object.message.get('from_id')
        peer_id = event.object.message.get('peer_id')
        self.notifier.notify(peer_id,
                             _(f"""
                      Ваш ID (user_id/from_id): {user_id}
                      ID группы (group_id): {event.group_id}
                      ID чата/беседы (peer_id): {peer_id}
                      """))

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()