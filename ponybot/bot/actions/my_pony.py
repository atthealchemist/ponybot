from bot.actions.create_pony import ActionCreatePony
from django.utils.translation import gettext as _

from pony.models import Pony

from .base import SimpleAction


class ActionMyPonyProfile(SimpleAction):

    def __init__(self, notifier=None):
        super().__init__(notifier)

        self.aliases = [
            'моя пони',
            'мои пони',
            'пони профиль'
        ]

    def call(self, event):
        user_id = event.object.message.get('from_id')
        peer_id = event.object.message.get('peer_id')

        user_ponies = Pony.objects.filter(owner=user_id)
        if not user_ponies.exists():
            self.notifier(peer_id, _(
                f"У вас ещё нет ни одной пони!\nЗаведите её, написав одну из следующих команд: {str(ActionCreatePony())}"
            ))
            return
        if user_ponies.count() > 1:
            user_id = event.object.message.get('from_id')

        self.notifier(user_id if user_ponies.count() > 1 else peer_id,
                      _(f"Ваши пони:\n" +
                      '\n'.join([f"{i + 1}. {str(p)}" for i, p in enumerate(user_ponies)])))
