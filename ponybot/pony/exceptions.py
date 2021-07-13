from django.utils.translation import gettext as _

from constance import config


class PonyException(Exception):
    def __init__(self, pony=None):
        self.message = None
        self.pony = pony
        self.pony_name = pony.name if pony else ""


class PonyDeadException(PonyException):
    def __init__(self, pony=None):
        super().__init__(pony=pony)

    def __str__(self):
        return _(f"Ваша пони {self.pony_name} мертва, все её действия отключены.")


class PonyOverfeedException(PonyException):
    def __init__(self, pony=None):
        super().__init__(pony=pony)

    def __str__(self):
        return _(f"Ваша пони {self.pony_name} объелась и не может больше есть")


class PonyFeedingTimeoutException(PonyException):
    def __init__(self, pony=None):
        super().__init__(pony=pony)

    def __str__(self):
        return _(f"Ваша пони {self.pony_name} ела совсем недавно, попробуйте через {config.PONY_FEEDING_TIMEOUT_MINS} минут...")


class PonyTiredException(PonyException):
    def __init__(self, pony=None):
        super().__init__(pony=pony)

    def __str__(self):
        return _(f"Ваша пони {self.pony_name} слишком устала, попробуйте через {config.PONY_LEARNING_TIMEOUT_MINS} минут...")
