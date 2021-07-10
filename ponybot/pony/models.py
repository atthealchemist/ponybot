import uuid
from django.utils import timezone
from string import Template

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
    last_learning = models.DateTimeField(
        null=True, auto_now=True
    )
    is_alive = models.BooleanField(_("Is pony alive"), default=True)

    def reset_stats(self):
        self.satiety = 0
        self.experience = 0
        self.save(update_fields=['satiety', 'experience'])

    def die(self):
        self.reset_stats()
        self.is_alive = False
        self.save(update_fields=['is_alive'])

    def feed(self):
        if any([self.satiety >= self.experience * 14, not self.is_alive]):
            return
        self.first_feeding = timezone.now()
        self.satiety += 1
        self.save(update_fields=['satiety', 'first_feeding'])

    def learn(self):
        pass

    def __str__(self):
        pony_stats_template = Template(
            """
            Name: $name
            Experience: $experience
            Satiety: $satiety
            """
        )

        return _(pony_stats_template.safe_substitute(
            name=self.name,
            experience=self.experience,
            satiety=self.satiety
        ))
