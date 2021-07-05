from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Pony(models.Model):
    name = models.CharField(_("Pony name"), max_length=64, blank=True)
