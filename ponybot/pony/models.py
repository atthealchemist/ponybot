from bot.utils import humanize_time, timedelta_to_time
from pony.exceptions import PonyDeadException, PonyFeedingTimeoutException, PonyOverfeedException, PonyTiredException
import uuid
from string import Template
from datetime import datetime, timedelta

from django.db import models
from django.db.models.enums import TextChoices

from django.utils import timezone
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator

from constance import config

# Create your models here.


class Race(TextChoices):
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
    name = models.CharField(_("Name"), max_length=64, blank=True)
    race = models.CharField(
        _("Race"), max_length=12, choices=Race.choices, default=Race.EARTHPONY)
    experience = models.PositiveSmallIntegerField(
        _("Level"),
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    satiety = models.PositiveSmallIntegerField(
        _("Satiety"),
        default=10
    )
    last_feeding = models.DateTimeField(
        _("Last feeding"),
        null=True, auto_now=True
    )
    last_learning = models.DateTimeField(
        _("Last learning"),
        null=True, auto_now=True
    )
    is_alive = models.BooleanField(_("Is alive"), default=True)

    owner = models.CharField(
        _("Owner"),
        max_length=16,
        null=True,
        blank=True
    )
    conversation = models.CharField(
        _("Conversation"), max_length=16, null=True, blank=True)

    avatar_url = models.CharField(
        _("Avatar"), max_length=256, null=True, blank=True
    )

    def set_race(self, race):
        self.race = Race.from_user_choice(race)
        self.save(update_fields=['race'])

    def set_owner(self, owner_id):
        self.owner = str(owner_id)
        self.save(update_fields=['owner'])

    def set_conversation(self, peer_id):
        self.conversation = peer_id
        self.save(update_fields=['conversation'])

    def set_avatar(self, avatar_url):
        self.avatar_url = avatar_url
        self.save(update_fields=['avatar_url'])

    def reset_stats(self):
        self.satiety = 0
        self.experience = 0
        self.save(update_fields=['satiety', 'experience'])

    def die(self):
        self.reset_stats()
        self.is_alive = False
        self.save(update_fields=['is_alive'])

    def feed(self):
        if not self.is_alive:
            raise PonyDeadException(self)

        feeding_timeout = config.PONY_FEEDING_TIMEOUT_MINS
        if self.satiety >= self.experience * 14:
            raise PonyOverfeedException(self)

        # Пони покормили в 10:30 (last_feeding)
        # Сейчас 10:34 (now)
        # Её следующая покормка (next_feeding) - 10:30 (last_feeding) + 8 минут (timeout) = 10:38
        next_feeding = self.last_feeding + timedelta(minutes=feeding_timeout)
        # Осталось времени до покормки - next_feeding - now
        time_to_feed = next_feeding - timezone.now()
        # Если осталось время для покормки - выбрасываем exception
        try:
            if timedelta_to_time(time_to_feed) < next_feeding.time():
                raise PonyFeedingTimeoutException(self)
        except OverflowError:
            # Для случаев, если пони кормили пару дней назад
            pass

        # Иначе кормим пони
        self.satiety += 1
        # Как только мы покормили пони, устанавливаем время последней покормки - сейчас
        self.last_feeding = timezone.now()
        self.save(update_fields=['satiety', 'last_feeding'])

    def learn(self):
        if not self.is_alive:
            raise PonyDeadException(self)

        learning_timeout = config.PONY_LEARNING_TIMEOUT_MINS

        next_learning = self.last_learning + \
            timedelta(minutes=learning_timeout)
        time_to_learn = next_learning - timezone.now()
        try:
            if timedelta_to_time(time_to_learn) < next_learning.time():
                raise PonyTiredException(self)
        except OverflowError:
            pass

        points = self.satiety + (abs(10 - self.satiety) / 2) - 5

        self.experience += int(points)
        self.last_learning = timezone.now()
        self.save(update_fields=['experience', 'last_learning'])

        return points

    def __str__(self):
        fields = [
            f"{f.verbose_name}: {f.value_from_object(self)}" for f in self._meta.fields]
        print('fields', fields)
        pony_stats_template = Template(
            """
            🐎\tName: $name $dead
            👬\tRace: $sex
            📖\tLevel: $experience
            🍎\tSatiety: $satiety
            ---
            👥\tOwner: $owner
            💬\tConversation: $conversation
            ---
            📚\tLast learning: $last_learning
            🍼\tLast feeding: $last_feeding
            """
        )

        return _(pony_stats_template.safe_substitute(
            name=self.name.capitalize(),
            dead=_("(мертва)") if not self.is_alive else "",
            sex=self.race,
            experience=self.experience,
            satiety=self.satiety,
            owner=self.owner,
            conversation=self.conversation,
            last_learning=humanize_time(self.last_learning),
            last_feeding=humanize_time(self.last_feeding)
        ))

    class Meta:
        verbose_name = "Pony"
        verbose_name_plural = "Ponies"
        ordering = ('owner', 'name',  'last_feeding', 'last_learning')
