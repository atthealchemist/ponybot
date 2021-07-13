from pony.exceptions import PonyException
from bot.actions.create_pony import ActionCreatePony
from django.utils.translation import gettext as _

from pony.models import Pony

from .base import SimpleAction


class ActionFeedPony(SimpleAction):
    aliases = (
        'кормить пони',
        'покормить пони',
        'покормить',
        'покушать'
    )

    def __init__(self, bot):
        super().__init__(bot=bot)

    def call(self, user_id, peer_id, message, event):
        user_ponies = Pony.objects.filter(
            owner=user_id,
            conversation=peer_id,
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
            self.bot.say(
                peer_id,
                message=_(
                    f"Ваша пони ({user_pony.name.capitalize()}) покушала и теперь её сытость равна {user_pony.satiety}"),
                prefix='🍼'
            )
        except PonyException as ex:
            self.bot.warn(peer_id, ex)
