from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model


from .base import SimpleAction


class ActionMySubs(SimpleAction):
    aliases = (
        'мои подписки',
        'моя подписка'
    )

    def __init__(self, bot=None):
        super().__init__(bot)

    def call(self, session, message, event):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=session.user_id)
            is_subscribed = all(
                [user.is_subscriber, user.subscribed_at])
            sub = f"действует с {user.subscribed_at.date()}" if is_subscribed else "отсутствует"
            self.bot.say(session, _(
                f"Ваша подписка: {sub}"), prefix="💳" if is_subscribed else "")
        except user_model.DoesNotExist:
            self.bot.warn(session, _(
                "У вас не существует профиля! Заведите его, создав новую пони."))
            return
