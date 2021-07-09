from bot.actions.create_pony import ActionCreatePony
from django.utils.translation import gettext as _

from pony.models import Pony

from .base import DialogAction


class ActionKillPony(DialogAction):

    def __init__(self, notifier=None):
        super().__init__(notifier)

        self.aliases = [
            'убить пони',
            'тетрадь смерти'
        ]

    def call(self, event):
        user_id = event.object.message.get('from_id')
        peer_id = event.object.message.get('peer_id')

        pony_to_kill = self.ask(
            peer_id,
            _("Впишите имя пони, которая должна умереть")
        )

        dead_pony = Pony.objects.filter(
            name__icontains=pony_to_kill, owner=user_id)
        if not dead_pony.exists():
            self.notifier.notify(peer_id, _(
                f"Такой пони не существует у {user_id}"))
            return
        dead_pony = dead_pony.first()

        dead_pony.die()
        self.notifier.notify(peer_id, _(f"Пони {dead_pony.name} умерла."))
