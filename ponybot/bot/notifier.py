from django.conf import settings

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.utils import get_random_id

from abc import ABC as AbstractBase, abstractmethod


class Notifier(AbstractBase):

    @abstractmethod
    def notify(self, sender, message):
        pass


class VkNotifier(Notifier):

    def notify(self, sender, message, attachment=None):
        self.api.messages.send(
            peer_id=sender,
            message=message,
            random_id=get_random_id(),
            attachment=attachment
        )

    def __init__(self):
        self.session = VkApi(
            token=settings.VK_API_TOKEN,
        )
        self.long_poll = VkBotLongPoll(self.session, settings.VK_GROUP_ID)
        self.api = self.session.get_api()
