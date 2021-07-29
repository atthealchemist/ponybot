from .base import SimpleAction
from django.utils.translation import gettext as _


class ActionGetId(SimpleAction):
    aliases = (
        'мой ид',
        'мой id'
    )

    def __init__(self, bot):
        super().__init__(bot)

    def call(self, session, message, event):
        self.say(session,
                 _(f"""
                        Ваш ID (user_id/from_id): {session.user_id}
                        ID группы (group_id): {event.group_id}
                        ID чата/беседы (peer_id): {session.peer_id}
                        """))

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()
