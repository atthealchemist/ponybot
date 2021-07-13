from bot.actions.create_pony import ActionCreatePony
from django.utils.translation import gettext as _

from pony.models import Pony

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

    def call(self, user_id, peer_id, message, event):
        user_ponies = Pony.objects.filter(owner=user_id, is_alive=True)
        if not user_ponies.exists():
            self.bot.warn(peer_id, _(
                f"У вас ещё нет ни одной пони!\nЗаведите её, написав одну из следующих команд: {str(ActionCreatePony())}"
            ))
            return

        self.bot.say(peer_id, _(f"Ваши пони:\n"))
        for idx, pony in enumerate(user_ponies):
            self.bot.say(
                peer_id,
                message=f"{idx + 1}. {str(pony)}",
                attachment=pony.avatar_url if pony.avatar_url else ""
            )
