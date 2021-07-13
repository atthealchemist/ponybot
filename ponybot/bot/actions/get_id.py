from .base import SimpleAction
from django.utils.translation import gettext as _


class ActionGetId(SimpleAction):
    aliases = (
        'мой ид',
        'мой id'
    )

    def __init__(self, bot):
        super().__init__(bot)

    def call(self, user_id, peer_id, message, event):
        self.say(peer_id,
                 _(f"""
                        Ваш ID (user_id/from_id): {user_id}
                        ID группы (group_id): {event.group_id}
                        ID чата/беседы (peer_id): {peer_id}
                        """))

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()
