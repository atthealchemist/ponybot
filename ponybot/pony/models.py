from datetime import timedelta
from pony.exceptions import PonyOverfeedException, PonyTiredException
import uuid
from django.db.models.enums import TextChoices

from django.utils import timezone
from string import Template

from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator

from constance import config

# Create your models here.


class PonySex(TextChoices):
    EARTHPONY = _("Земнопони")
    PEGASUS = _("Пегас")
    UNICORN = _("Единорог")
    ALICORN = _("Аликорн")

    @classmethod
    def choice_list(cls):
        return [c.value.lower() for c in cls.values]

    @classmethod
    def from_user_choice(cls, choice):
        mapping = {
            'пегас': cls.PEGASUS,
            'земнопони': cls.EARTHPONY,
            'единорог': cls.UNICORN,
            'аликорн': cls.ALICORN
        }
        return mapping.get(choice)

class Pony(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Pony name"), max_length=64, blank=True)
    sex = models.CharField(
        _("Pony sex"), max_length=12, choices=PonySex.choices, default=PonySex.EARTHPONY)
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
    last_feeding = models.DateTimeField(null=True, auto_now=True)
    last_learning = models.DateTimeField(null=True, auto_now=True)
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

    def set_name(self, new_name):
        self.name = new_name
        self.save(update_fields=['name'])

    def reset_stats(self):
        self.satiety = 0
        self.experience = 0
        self.save(update_fields=['satiety', 'experience'])

    def learn(self):
        learning_timeout = config.PONY_LEARNING_TIMEOUT_MINS
        if self.last_learning < self.last_learning + timedelta(minutes=learning_timeout):
            raise PonyTiredException(
                f"Ваша пони ({self.name}) слишком устала, попробуйте через {learning_timeout} минут...")
        points = self.satiety + (abs(10 - self.satiety) / 2) - 5

        self.experience += points
        self.last_learning = timezone.now()
        self.save(update_fields=['experience', 'last_learning'])

        return points

    def hunger(self):
        self.satiety -= 1
        self.save(update_fields=['satiety'])

    def die(self):
        self.reset_stats()
        self.is_alive = False
        self.save(update_fields=['is_alive'])

    def feed(self):
        feeding_timeout = config.PONY_FEEDING_TIMEOUT_MINS
        if self.satiety >= self.experience * 14:
            raise PonyOverfeedException(
                "Ваша пони объелась и не может больше есть")
        if self.last_feeding < self.last_feeding + timedelta(minutes=feeding_timeout):
            raise PonyOverfeedException(
                f"Ваша пони ({self.name}) ела совсем недавно ({self.last_feeding}), попробуйте через {feeding_timeout} минут...")
        self.last_feeding = timezone.now()
        self.satiety += 1
        self.save(update_fields=['satiety', 'last_feeding'])

    def __str__(self):
        pony_stats_template = Template(
            """
            Name: $name $dead
            Sex: $sex
            Experience: $experience
            Satiety: $satiety
            ---
            Owner: $owner
            Conversation: $conversation
            ---
            Last learning: $last_learning
            Last feeding: $last_feeding
            """
        )

        return _(pony_stats_template.safe_substitute(
            name=self.name,
            dead=_("(мертва)") if not self.is_alive else "",
            sex=self.sex,
            experience=self.experience,
            satiety=self.satiety,
            owner=self.owner,
            conversation=self.conversation,
            last_learning=self.last_learning,
            last_feeding=self.last_feeding
        ))

    class Meta:
        verbose_name = "Pony"
        verbose_name_plural = "Ponies"
        ordering = ('owner', 'name',  'last_feeding', 'last_learning')
