from django.utils.translation import gettext as _
from django.utils.crypto import get_random_string

from django.contrib.auth import get_user_model

from .base import DialogAction, UploadPhotoAction
from pony.models import Pony

from constance import config


class ActionCreatePony(DialogAction, UploadPhotoAction):

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

        user_model = get_user_model()

        try:
            user = user_model.objects.get(username=user_id)
        except user_model.DoesNotExist:
            user = user_model.objects.create(
                username=user_id,
                password=get_random_string(32)
            )

        if Pony.objects.filter(owner=user.username, conversation=peer_id, is_alive=True).exists():
            self.notifier.notify(peer_id, _(
                "Вы не можете иметь более одной пони в беседе!"))
            return

        pony_info['name'] = self.ask(
            user_id,
            question=_("Как вы хотите назвать вашу пони?"),
            answer_message=_("Вашу пони теперь зовут: {0}")
        )

        pony_info['sex'] = self.choice(
            user_id,
            question=_(f"Выберите расу вашей пони: "),
            choices=['пегас', 'единорог', 'земнопони']
        )

        pony_info['avatar_url'] = self.ask_photo(
            user_id,
            question=_(
                "Прикрепите аватар вашей пони (нажмите на скрепочку и выберите фото):"),
            declines=['-', 'нет', 'не надо']
        )

        new_pony = Pony.objects.create(**pony_info)
        new_pony.set_owner(user_id)
        new_pony.set_conversation(peer_id)
        new_pony.set_sex(pony_info.get('sex'))

        if 'avatar_url' in pony_info:
            new_pony.set_avatar(pony_info.get('avatar_url'))

        self.notifier.notify(
            peer_id,
            _(f"Ваша пони:  {new_pony}"),
            attachment=new_pony.avatar_url if new_pony.avatar_url else ""
        )

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()
