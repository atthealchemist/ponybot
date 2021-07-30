from django.db import models

import uuid
import math
from string import Template
from datetime import timedelta

from django.db import models
from django.db.models.enums import TextChoices

from django.utils import timezone
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator

from constance import config

from core.utils import humanize_time, timedelta_to_time
from core.exceptions import PonyDeadException, PonyFeedingTimeoutException, PonyOverfeedException, PonyTiredException

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


class Gender(TextChoices):
    STALLION = _("Жеребец")
    MARE = _("Кобылка")

    @classmethod
    def choice_list(cls):
        return [c.value.lower() for c in cls.values]

    @classmethod
    def from_user_choice(cls, choice):
        mapping = {
            'жеребец': cls.STALLION,
            'кобылка': cls.MARE
        }
        return mapping.get(choice)


class Pony(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name"), max_length=64, blank=True)
    race = models.CharField(
        _("Race"), max_length=12, choices=Race.choices, default=Race.EARTHPONY)
    gender = models.CharField(
        _("Gender"), max_length=10, choices=Gender.choices, default=Gender.STALLION)
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
        null=True, auto_now=False
    )
    last_learning = models.DateTimeField(
        _("Last learning"),
        null=True, auto_now=False
    )
    is_alive = models.BooleanField(_("Is alive"), default=True)

    owner = models.CharField(
        _("Owner"),
        max_length=16,
        null=True,
        blank=True
    )

    owner_title = models.CharField(
        _("Owner title"), max_length=128, null=True, blank=True)

    conversation = models.CharField(
        _("Conversation"), max_length=16, null=True, blank=True)

    conversation_title = models.CharField(
        _("Conversation title"), max_length=128, null=True, blank=True)

    avatar_url = models.CharField(
        _("Avatar"), max_length=256, null=True, blank=True
    )

    def set_race(self, race):
        self.race = Race.from_user_choice(race)
        self.save(update_fields=['race'])
    
    def set_gender(self, gender):
        self.gender = Gender.from_user_choice(gender)
        self.save(update_fields=['gender'])

    def set_owner(self, owner_id, title=''):
        self.owner = str(owner_id)
        self.owner_title = title
        self.save(update_fields=['owner', 'owner_title'])

    def set_conversation(self, peer_id, title=''):
        self.conversation = peer_id
        self.conversation_title = title
        self.save(update_fields=['conversation', 'conversation_title'])

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

    @property
    def owner_alloc(self):
        return f"[id{self.owner}|{self.owner_title}]"
    
    @property
    def short_name(self):
        return ' '.join([n.capitalize() for n in self.name.split(' ')])

    @property
    def full_name(self):
        return f'{self.name} из беседы "{self.conversation_title}"'
    
    def hunger(self):
        self.satiety -= 1
        if self.satiety < 1:
            self.die()
        self.save(update_fields=['satiety'])

    def feed(self):
        if not self.is_alive:
            raise PonyDeadException(self)

        feeding_timeout = config.PONY_FEEDING_TIMEOUT_MINS
        if self.satiety >= self.experience * 14:
            raise PonyOverfeedException(self)

        # Пони покормили в 10:30 (last_feeding)
        # Сейчас 10:34 (now)
        # Её следующая покормка (next_feeding) - 10:30 (last_feeding) + 8 минут (timeout) = 10:38
        if self.last_feeding:
            next_feeding = self.last_feeding + \
                timedelta(minutes=feeding_timeout)
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

        if self.last_learning:
            next_learning = self.last_learning + \
                timedelta(minutes=learning_timeout)
            time_to_learn = next_learning - timezone.now()
            try:
                if timedelta_to_time(time_to_learn) < next_learning.time():
                    raise PonyTiredException(self)
            except OverflowError:
                pass
        
        # Сытость + |10 - Сытость|
        # ------------------------ - 5
        #           2
        # Исходная формула: (Сытость + |10 - Сытость|)/2-5
        points = (self.satiety + abs(10 - self.satiety) / 2) - 5

        self.experience += int(points)
        self.last_learning = timezone.now()
        self.save(update_fields=['experience', 'last_learning'])

        return points

    def __str__(self):
        fields = [
            f"{f.verbose_name}: {f.value_from_object(self)}" for f in self._meta.fields]
        # print('fields', fields)
        pony_stats_template = Template(
            """
            🐎\tИмя: $name $dead
            👬\tРаса: $race
            ⚤\tПол: $gender
            📖\tУровень: $experience
            🍎\tСытость: $satiety
            ---
            👥\tВладелец: $user
            💬\tБеседа: [id$conversation|$conversation_title]
            ---
            📚\tПоследний раз учили: $last_learning
            🍼\tПоследний раз кормили: $last_feeding
            """
        )

        last_learning = humanize_time(
            self.last_learning) if self.last_learning else _("ещё ни разу не учили")
        last_feeding = humanize_time(
            self.last_feeding) if self.last_feeding else _("ещё ни разу не кормили")

        return _(pony_stats_template.safe_substitute(
            name=self.short_name,
            dead=_("(мертва)") if not self.is_alive else "",
            race=self.race,
            gender=self.gender,
            experience=self.experience,
            satiety=self.satiety,
            user=self.owner_alloc,
            conversation_title=self.conversation_title,
            conversation=self.conversation,
            last_learning=last_learning,
            last_feeding=last_feeding
        ))

    class Meta:
        verbose_name = "Pony"
        verbose_name_plural = "Ponies"
        ordering = ('owner', 'name',  'last_feeding', 'last_learning')
