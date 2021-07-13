from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


from .base import DialogAction, UploadPhotoAction
from pony.models import Pony


class ActionCreatePony(DialogAction, UploadPhotoAction):
    aliases = (
        'создать пони',
        'завести пони'
    )

    def __init__(self, bot=None):
        super().__init__(bot)

    def call(self, user_id, peer_id, message, event):
        pony_info = dict()

        if Pony.objects.filter(owner=user_id, conversation=peer_id, is_alive=True).exists():
            self.bot.warn(peer_id, _(
                "Вы не можете иметь более одной пони в беседе!"))
            return
        user = get_user_model().objects.get(username=user_id)

        pony_info['name'] = self.ask(
            peer_id,
            user=user,
            question=_("Как вы хотите назвать вашу пони?"),
            answer_message=_("Вашу пони теперь зовут: {0}")
        )

        pony_info['race'] = self.choice(
            peer_id,
            user=user,
            question=_(f"Выберите расу вашей пони: "),
            choices=['пегас', 'единорог', 'земнопони']
        )

        pony_info['avatar_url'] = self.ask_photo(
            peer_id,
            user=user,
            question=_(
                "Прикрепите аватар вашей пони (нажмите на скрепочку и выберите фото):"),
            declines=['-', 'нет', 'не надо']
        )

        new_pony = Pony.objects.create(**pony_info)
        new_pony.set_owner(user_id)
        new_pony.set_conversation(peer_id)
        new_pony.set_race(pony_info.get('race'))

        if 'avatar_url' in pony_info:
            new_pony.set_avatar(pony_info.get('avatar_url'))

        self.bot.say(peer_id, _(
            f"Ваша пони:  {new_pony}"), attachment=new_pony.avatar_url)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()
