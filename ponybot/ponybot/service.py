import vk_api
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from enum import Enum
from queue import Queue

from django.conf import settings
from django.utils.translation import gettext as _

import configurations


class Command:

    def call(self, event):
        sender = event.object.message.get('from_id')
        message = event
        self.callback(sender, message)

        # bot.state = self.state
        # self.sender = sender
        # print(f"[{self.sender}] Set new state to bot: {bot.state}")

    def __init__(self, aliases, callback):
        self.aliases = aliases

        self.callback = callback


class PonybotState(Enum):
    IDLE = "IDLE"
    CREATE = "CREATE"
    RENAME = "RENAME"
    FEED = "FEED"


class PonybotService:

    # def rename_pony(self, user_id, command, message):
    #     # pony_name = message.index("")
    #     self.__send(user_id, f"Как назвать твою пони?")

    def on_rename_pony(self, sender, message):
        self.send_from_bot(sender, "Как назвать вашу пони?")
        self.state = PonybotState.RENAME
        print('state', self.state)

    def on_rename_pony_finish(self, sender, new_name, message):
        self.send_from_bot(sender, f"Вашу пони теперь зовут {new_name}!")
        self.state = PonybotState.IDLE
        print('state', self.state)

    def on_feed_pony(self, sender, message):
        pass

    def create_pony(self, sender, message):
        self.send_from_bot(sender, "Нужно придумать для вашей пони имя")

    def get_id(self, sender, message):
        self.send_from_bot(
            sender,
            f"Ваш ID: {message.object.get('message').get('from_id')}\nID группы: {message.group_id}"
        )

    def __init__(self, token, group_id):
        self.session = VkApi(
            token=token
        )
        self.long_poll = VkBotLongPoll(self.session, group_id)
        self.api = self.session.get_api()

        self.state = PonybotState.IDLE
        self.is_running = False

        self.available_commands = [
            Command(
                aliases=[
                    'создать пони',
                    'новая пони',
                    'взять пони',
                    'завести пони'
                ],
                callback=self.create_pony
            ),
            Command(
                aliases=['дать пони имя', 'назвать пони'],
                callback=self.on_rename_pony
            ),
            Command(
                aliases=['покормить пони'],
                callback=self.on_feed_pony
            ),
            Command(
                aliases=['узнать id', 'мой id', 'узнать ид', 'мой ид'],
                callback=self.get_id
            )
        ]

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.__process()

    def send_from_bot(self, user_id, message):
        self.api.messages.send(
            user_id=user_id,
            message=message,
            random_id=get_random_id()
        )

    def on_bot_send_event(self, event):
        print('message_reply evt', event)
        message_obj = event.object
        from_id = message_obj.get('from_id')
        user_id = message_obj.get('peer_id')
        message = message_obj.get('text')
        print(f'bot {from_id} reply: {message}')

    def on_user_send_event(self, event):
        print('message_new evt', event)
        message_obj = event.object.message
        from_id = message_obj.get('from_id')
        message = message_obj.get('text')
        from_user = message_obj.get('out') == 0
        print(f'got new message from user {from_id}: {message}')

        for cmd in self.available_commands:
            if any([a for a in cmd.aliases if message in a]):
                cmd.call(event)
                return

        if self.state == PonybotState.RENAME:
            if from_user:
                self.on_rename_pony_finish(from_id, message_obj)

    def __process(self):
        if not self.is_running:
            return

        print("Started vk bot, listening...")

        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                self.on_user_send_event(event)

            elif event.type == VkBotEventType.MESSAGE_REPLY:
                self.on_bot_send_event(event)

    def stop(self):
        if self.is_running:
            self.is_running = False


if __name__ == "__main__":
    configurations.setup()
    bot = PonybotService(
        token=settings.VK_API_TOKEN,
        group_id=settings.VK_GROUP_ID
    )
    bot.start()
