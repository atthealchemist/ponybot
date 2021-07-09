from django.utils.translation import gettext as _

from .base import DialogAction
from pony.models import Pony, PonySex


class ActionCreatePony(DialogAction):

    def __init__(self, notifier=None):
        self.notifier = notifier

        self.aliases = [
            'создать пони',
            'завести пони'
        ]

    def call(self, event):
        pony_info = dict()

        user_id = event.object.message.get('from_id')
        peer_id = event.object.message.get('peer_id')

        if Pony.objects.filter(owner=user_id, conversation=peer_id, is_alive=True).exists():
            self.notifier.notify(peer_id, _(
                "Вы не можете иметь более одной пони в беседе!"))
            return

        pony_info['name'] = self.ask(
            peer_id,
            question=_("Как вы хотите назвать вашу пони?"),
            answer_message=_("Вашу пони теперь зовут: {0}")
        )

        pony_info['sex'] = PonySex.from_user_choice(self.choice(
            peer_id,
            question=_(f"Выберите расу вашей пони: "),
            choices=['пегас', 'единорог', 'земнопони']
        ))

        new_pony = Pony.objects.create(**pony_info)
        new_pony.set_owner(user_id)
        new_pony.set_conversation(peer_id)

        self.notifier.notify(
            peer_id,
            _(f"Ваша пони:  {new_pony}")
        )

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()
