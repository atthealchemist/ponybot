from bot.notifier import VkNotifier
import logging
import pkgutil
import inspect
import importlib

from django.utils.translation import gettext as _
from django.utils import timezone
from django.conf import settings

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.utils import get_random_id


class PonybotService:

    def __init__(self, private=False):
        # self.session = VkApi(
        #     token=settings.VK_API_TOKEN,
        # )
        # self.long_poll = VkBotLongPoll(self.session, settings.VK_GROUP_ID)
        # self.api = self.session.get_api()

        self.notifier = VkNotifier()

        self.is_running = False
        self.case_sensitive = False
        self.private = private

        self.logger = logging.getLogger("Ponybot")

        self.actions = [
            action_cls(
                notifier=self.notifier
            ) for action_cls in self.load_actions()
        ]

    def load_actions(self):
        actions = []

        # find all action modules
        search_path = ['bot/actions/']
        all_actions = [
            a
            for _, a, *_
            in pkgutil.iter_modules(path=search_path)
        ]

        # load all modules
        for action in all_actions:
            if action == 'base':
                continue
            module_path = f'bot.actions.{action}'
            action_classes = [
                _cls
                for _, _cls in inspect.getmembers(importlib.import_module(module_path), inspect.isclass)
                if _cls.__module__ == module_path
            ]
            actions += action_classes

        return actions

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.logger.debug(
                f"Auto loaded actions: {self.actions}")
            self.__process()

    # def send_from_bot(self, peer_id, message):
    #     self.api.messages.send(
    #         peer_id=peer_id,
    #         message=message,
    #         random_id=get_random_id()
    #     )

    def on_bot_send_event(self, event):
        self.logger.debug(f'message_reply evt {event}')
        message_obj = event.object
        from_id = message_obj.get('from_id')
        message = message_obj.get('text')
        self.logger.debug(f'bot {from_id} reply: {message}')

    def on_user_send_event(self, event):
        self.logger.debug(f'message_new evt {event}')
        message_obj = event.object.message
        from_id = message_obj.get('from_id')
        peer_id = message_obj.get('peer_id')
        message = message_obj.get('text')
        self.logger.debug(
            f'got new message from user {from_id} [peer {peer_id}]: {message}')

        for action in self.actions:
            if any([a for a in action.aliases if message.lower() in a.lower()]):
                action.call(event)
                return
        # else:
        #     self.send_from_bot(peer_id,
        #                        _(f'Команда "{message}" не распознана!\nДоступные команды:\n'
        #                          + "\n".join([f"{i + 1}. {str(a)}" for i, a in enumerate(self.actions)])))

    def __process(self):
        if not self.is_running:
            return

        self.logger.info(f"Started vk bot @ {timezone.now()}, listening...")
        try:
            for event in self.notifier.long_poll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if 'action' in event.object.message:
                        break
                    self.on_user_send_event(event)
                elif event.type == VkBotEventType.MESSAGE_REPLY:
                    self.on_bot_send_event(event)
        except KeyboardInterrupt:
            self.logger.info(f"Stopping vk bot @ {timezone.now()}, exiting...")

    def stop(self):
        if self.is_running:
            self.is_running = False
