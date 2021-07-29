from .utils import timedelta_to_time
from django.utils.translation import gettext as _
from django.utils import timezone
from datetime import timedelta

from constance import config


class PonyException(Exception):
    def __init__(self, pony=None):
        self.message = None
        self.pony = pony
        self.pony_name = pony.name if pony else ""


class PonyNotExist(PonyException):
    def __init__(self, pony=None):
        super().__init__(pony=pony)

    def __str__(self):
        from bot.actions.create_pony import ActionCreatePony
        return _(
            f"У вас ещё нет ни одной пони!\nЗаведите её, написав одну из следующих команд: {str(ActionCreatePony())}"
        )

class UserNotExist(PonyException):
    def __init__(self, pony=None):
        super().__init__(pony=pony)

    def __str__(self):
        return _("У вас не существует профиля! Заведите его, создав новую пони.")

class PonyDeadException(PonyException):
    def __init__(self, pony=None):
        super().__init__(pony=pony)

    def __str__(self):
        return _(f"Ваша пони ({self.pony_name}) мертва, все её действия отключены.")


class PonyOverfeedException(PonyException):
    def __init__(self, pony=None):
        super().__init__(pony=pony)

    def __str__(self):
        return _(f"Ваша пони ({self.pony_name}) объелась и не может больше есть")


class PonyFeedingTimeoutException(PonyException):
    def __init__(self, pony=None):
        super().__init__(pony=pony)

    def __str__(self):
        next_feeding = self.pony.last_feeding + \
            timedelta(minutes=config.PONY_FEEDING_TIMEOUT_MINS)
        time_to_feed = timedelta_to_time(
            next_feeding - timezone.now()
        ).strftime("%-M минут %-S секунд")
        return _(f"Ваша пони ({self.pony_name}) ела совсем недавно, попробуйте через {time_to_feed}...")


class PonyTiredException(PonyException):
    def __init__(self, pony=None):
        super().__init__(pony=pony)

    def __str__(self):
        next_learning = self.pony.last_learning + \
            timedelta(minutes=config.PONY_LEARNING_TIMEOUT_MINS)
        time_to_learn = timedelta_to_time(
            next_learning - timezone.now()
        ).strftime("%-M минут %-S секунд")
        return _(f"Ваша пони ({self.pony_name}) слишком устала, попробуйте через {time_to_learn}...")
