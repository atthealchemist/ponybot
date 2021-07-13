from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

from constance import config


class PonybotUser(AbstractUser):
    is_subscriber = models.BooleanField(
        _("Is Subscriber"), default=False
    )
    subscribed_at = models.DateTimeField(
        _("Subscribed At"), auto_now=False, auto_now_add=False, null=True)

    class Meta:
        verbose_name = "Ponybot User"
        verbose_name_plural = "Ponybot Users"

    def is_admin(self, user_id):
        return self.is_superuser() or str(user_id) in config.PONY_BOT_ADMINS_LIST.split(',')

    def set_name(self, first_name="", last_name=""):
        self.first_name = first_name
        self.last_name = last_name
        self.save(update_fields=['first_name', 'last_name'])


class PonybotAction(models.Model):
    name = models.CharField(_("Action Name"), max_length=64)
    aliases = models.JSONField(_("Action aliases"), default=list)

    is_admin_only = models.BooleanField(_("Is admin only"), default=False)

    class Meta:
        verbose_name = "Ponybot Action"
        verbose_name_plural = "Ponybot Actions"
