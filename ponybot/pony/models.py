from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Pony(models.Model):
    name = models.CharField(_("Pony name"), max_length=64, blank=True)
    experience = models.PositiveSmallIntegerField(
        _("Pony experience"),
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
