import logging
import pkgutil
import inspect
import importlib

from bot.api import BotVkAPI
from django.utils.crypto import get_random_string

from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.auth import get_user_model


from .models import DialogSession, PonybotAction, PonybotUser


class PonybotService:

    def __init__(self):
        self.bot = BotVkAPI()
        self.is_running = False

        self.logger = logging.getLogger("Ponybot")

        self.actions = []

    def initialize_actions(self):
        for action_cls in self.load_actions():
            action_instance = action_cls(bot=self.bot)
            try:
                PonybotAction.objects.get(
                    name=action_instance.action_id
                )
            except PonybotAction.DoesNotExist:
                PonybotAction.objects.create(
                    name=action_instance.action_id,
                    aliases=action_instance.aliases,
                    is_admin_only=False
                )
            self.logger.info(f"Initialized {action_instance} in database")
            self.actions.append(action_instance)

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

    def initialize_user(self, user_id):
        try:
            called_user = get_user_model().objects.get(username=user_id)
        except PonybotUser.DoesNotExist:
            called_user = get_user_model().objects.create(
                username=user_id,
                password=get_random_string(32)
            )
        return called_user

    def cleanup_opened_sessions(self):
        DialogSession.objects.all().delete()

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.logger.debug(
                f"Auto loaded actions: {self.actions}")
            self.initialize_actions()
            self.cleanup_opened_sessions()

            self.logger.info(
                f"Started vk bot @ {timezone.now()}, listening...")
            try:
                for user_id, peer_id, message, event in self.bot.listen_new_messages():
                    self.listen_message_from_user(
                        user_id, peer_id, message, event)
            except KeyboardInterrupt:
                self.logger.info(
                    f"Stopping vk bot @ {timezone.now()}, exiting...")
                self.stop()

    def listen_message_from_user(self, user_id, peer_id, message, event):
        self.logger.debug(
            f'got new message from user {user_id} [peer {peer_id}]: {message}')

        for action in self.actions:
            related_action = PonybotAction.objects.get(name=action.action_id)
            called_user = self.initialize_user(user_id)

            if any([
                alias
                for alias in related_action.aliases
                if message.lower() in alias.lower()
            ]):
                if related_action.is_admin_only and not called_user.is_admin():
                    self.warn(peer_id, _(
                        "У вас недостаточно прав для доступа к этой команде!"))
                    return
                active_session = DialogSession.objects.create(
                    action_id=action.action_id,
                    peer_id=peer_id,
                    user_id=user_id
                )
                self.bot.logger.debug(f"Opened new {active_session}")
                action.call(
                    session=active_session,
                    message=message,
                    event=event
                )
                self.bot.logger.debug(f"Closed {active_session}")
                active_session.close()
                return

    def stop(self):
        if self.is_running:
            self.is_running = False
