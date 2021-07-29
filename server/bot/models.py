from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class BotAction(models.Model):
    name = models.CharField(_("Action Name"), max_length=64)
    aliases = models.JSONField(_("Action aliases"), default=list)

    is_admin_only = models.BooleanField(_("Is admin only"), default=False)

    class Meta:
        verbose_name = "Ponybot Action"
        verbose_name_plural = "Ponybot Actions"


class DialogSession(models.Model):
    user_id = models.CharField(
        _("User Id"), max_length=16, null=True, blank=True)
    peer_id = models.CharField(
        _("Peer Id"), max_length=16, null=True, blank=True)
    action_id = models.CharField(
        _("Action Id"), max_length=64, null=True, blank=True)

    last_message = models.JSONField(_("Last Message"), default=dict)

    opened = models.BooleanField(_("Opened"), default=True)

    class Meta:
        verbose_name = "Dialog Session"
        verbose_name_plural = "Dialog Sessions"

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"DialogSession #{self.pk} for user={self.user_id} in room={self.peer_id} performing action={self.action_id}"

    def close(self):
        if not self.opened:
            return
        self.opened = False
        self.save(update_fields=['opened'])

    def set_last_message(self, user_id, peer_id, message):
        self.last_message = dict(
            user_id=user_id, peer_id=peer_id, message=message
        )
        self.save(update_fields=['last_message'])
