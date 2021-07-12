
from django.utils.translation import gettext_lazy as _
from bot.actions.base import SimpleAction, UploadPhotoAction

from pony.models import Pony


class ChangeAvatarAction(UploadPhotoAction):

    def call(self, event):
        user_id = event.object.message.get('from_id')
        peer_id = event.object.message.get('peer_id')

        photo = self.ask_photo(user_id, question=_("Прикрепите аватар вашей пони: "), declines=[
            'нет',
            'не надо',
            '-'
        ])

        my_pony = Pony.objects.filter(
            owner=user_id, conversation=peer_id, is_alive=True
        )
        if not my_pony.exists():
            self.notifier.notify(user_id, _("Такой пони не существует!"))
            return
        my_pony = my_pony.first()

        if my_pony.avatar_url:
            self.notifier.notify(user_id, _("Картинка уже установлена!"))
            return

        my_pony.set_avatar(photo)
        self.notifier.notify(user_id,
                             _(f"Ваша пони:\n{str(my_pony)}"),
                             attachment=my_pony.avatar_url)

    def __init__(self, notifier=None):
        super().__init__(notifier=notifier)

        self.aliases = [
            'установить картинку пони',
            'установить аватар',
            'установить картинку'
        ]
