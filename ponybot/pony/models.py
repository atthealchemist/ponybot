import uuid
from django.utils import timezone

from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Pony(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Pony name"), max_length=64, blank=True)
    experience = models.PositiveSmallIntegerField(
        _("Pony experience"),
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    satiety = models.PositiveSmallIntegerField(
        _("Pony satiety"),
        default=10
    )
    first_feeding = models.DateTimeField(null=True, blank=True)
    last_feeding = models.DateTimeField(
        null=True, auto_now=True
    )

    def feed(self):
        if self.satiety >= self.experience * 14:
            return
        self.first_feeding = timezone.now()
        self.satiety += 1
        self.save(update_fields=['satiety', 'first_feeding'])
