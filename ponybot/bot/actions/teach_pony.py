from pony.exceptions import PonyException
from bot.actions.create_pony import ActionCreatePony
from django.utils.translation import gettext as _

from pony.models import Pony

from .base import SimpleAction


class ActionTeachPony(SimpleAction):
    aliases = (
        'учить пони',
        'отправиться в библиотеку',
        'пойти в библиотеку'
    )

    def __init__(self, bot):
        super().__init__(bot)

    def call(self, user_id, peer_id, message, event):
        user_ponies = Pony.objects.filter(
            owner=user_id, conversation=peer_id, is_alive=True)
        if not user_ponies.exists():
            self.warn(peer_id, _(
                f"У вас ещё нет ни одной пони!\nЗаведите её, написав одну из следующих команд: {str(ActionCreatePony())}"
            ))
            return
        user_pony = user_ponies.first()
        try:
            user_pony.learn()
            self.bot.say(
                peer_id,
                message=_(
                    f"Ваша пони ({user_pony.name.capitalize()}) учится! Теперь её опыт равен {user_pony.experience}"),
                prefix='📚'
            )
        except PonyException as ex:
            self.bot.warn(peer_id, ex)
