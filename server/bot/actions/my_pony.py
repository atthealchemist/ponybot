from core.exceptions import PonyNotExist
from django.utils.translation import gettext as _

from core.models import Pony

from .base import SimpleAction


class ActionMyPonyProfile(SimpleAction):
    aliases = (
        'моя пони',
        'мой пони',
        'мои пони',
        'пони профиль'
    )

    def __init__(self, bot=None):
        super().__init__(bot)

    def call(self, session, message, event):
        user_ponies = Pony.objects.filter(owner=session.user_id)
        if not user_ponies.exists():
            raise PonyNotExist()
        self.bot.say(session, _(f"Ваши пони:\n"))
        for idx, pony in enumerate(user_ponies):
            self.bot.say(
                session,
                message=f"{idx + 1}. {str(pony)}",
                mention=False,
                attachment=pony.avatar_url if pony.avatar_url else ""
            )
