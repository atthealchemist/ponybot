from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


from .base import DialogAction, DialogStep as Step, UploadPhotoAction
from core.models import Pony


class ActionCreatePony(DialogAction, UploadPhotoAction):
    aliases = (
        'создать пони',
        'завести пони'
    )

    def __init__(self, bot=None):
        super().__init__(bot)
        self.steps = (
            Step(
                func_name='ask',
                param_name="name",
                question=_(f"Как вы хотите назвать вашу пони?"),
                answer_message=_("Вашу пони теперь зовут: {0}")),
            Step(
                func_name='choice',
                param_name="race",
                question=_(f"Выберите расу вашей пони: "),
                choices=('пегас', 'единорог', 'земнопони')),
            Step(
                func_name='ask_photo',
                param_name="avatar_url",
                question=_(
                    "Прикрепите аватар вашей пони (нажмите на скрепочку и выберите фото):"),
                declines=('-', 'нет', 'не надо'))
        )

    def call(self, session, message, event):
        pony_info = dict()

        if Pony.objects.filter(owner=session.user_id, conversation=session.peer_id, is_alive=True).exists():
            self.bot.warn(session, _(
                "Вы не можете иметь более одной пони в беседе!"))
            return

        user = get_user_model().objects.get(username=session.user_id)
        user.set_name(*self.bot.get_user_name(session.user_id).split(' '))

        for step in self.steps:
            self.bot.logger.debug(f"Calling {step}")
            step_func = getattr(self, step.func_name)
            self.bot.logger.debug(f"Step function: {step_func}")
            step_result = step_func(
                session=session,
                **step.attrs
            )
            self.bot.logger.debug(f"Step result: {step_result}")
            if not step_result:
                return

            pony_info[step.param_name] = step_result

        if pony_info.keys():
            new_pony = Pony.objects.create(**pony_info)
            new_pony.set_owner(
                session.user_id, title=self.bot.get_user_name(session.user_id))
            new_pony.set_conversation(
                session.peer_id, title=self.bot.get_conversation_title(session.peer_id))
            new_pony.set_race(pony_info.get('race'))

            if 'avatar_url' in pony_info:
                new_pony.set_avatar(pony_info.get('avatar_url'))

            self.bot.say(session, _(
                f"Ваша пони:  {new_pony}"), attachment=new_pony.avatar_url)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()
