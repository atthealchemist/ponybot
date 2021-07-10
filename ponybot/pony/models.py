import uuid
from string import Template
from datetime import timedelta

from django.db import models
from django.utils import timezone
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
    last_feeding = models.DateTimeField(
        null=True, auto_now=True
    )
    last_learning = models.DateTimeField(
        null=True, auto_now=True
    )
    is_alive = models.BooleanField(_("Is pony alive"), default=True)

    owner = models.CharField(
        _("Owner user id"),
        max_length=16,
        null=True,
        blank=True
    )
    conversation = models.CharField(
        _("Conversation peer id"), max_length=16, null=True, blank=True)

    def set_owner(self, owner_id):
        self.owner = str(owner_id)
        self.save(update_fields=['owner'])

    def set_conversation(self, peer_id):
        self.conversation = peer_id
        self.save(update_fields=['conversation'])

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
        self.last_feeding = timezone.now()
        self.satiety += 1
        self.save(update_fields=['satiety', 'last_feeding'])

    def learn(self):
        learning_timeout = 30
        if self.last_learning < self.last_learning + timedelta(seconds=learning_timeout):
            return 0
        points = self.satiety + (abs(10 - self.satiety) / 2) - 5

        self.experience += points
        self.last_learning = timezone.now()
        self.save(update_fields=['experience', 'last_learning'])

        return points

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
