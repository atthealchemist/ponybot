from core.exceptions import PonyException, PonyNotExist
from django.utils.translation import gettext as _

from core.models import Pony

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

    def call(self, session, message, event):
        user_ponies = Pony.objects.filter(
            owner=session.user_id,
            conversation=session.peer_id,
            is_alive=True
        )
        if not user_ponies.exists():
            raise PonyNotExist()

        user_pony = user_ponies.first()
        user_pony.feed()
        self.bot.say(
            session,
            message=_(
                f"Ваша пони ({user_pony.name.capitalize()}) покушала и теперь её сытость равна {user_pony.satiety}"),
            prefix='🍼'
        )
