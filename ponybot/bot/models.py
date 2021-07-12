from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
# Create your models here.


class PonybotUser(AbstractUser):
    is_subscriber = models.BooleanField(
        _("Is Subscriber"), default=False
    )
    subscribed_at = models.DateTimeField(
        _("Subscribed At"), auto_now=False, auto_now_add=False, null=True)

    class Meta:
        verbose_name = "Ponybot User"
        verbose_name_plural = "Ponybot Users"
