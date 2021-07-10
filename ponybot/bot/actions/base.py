from abc import ABC as AbstractBase, abstractmethod

from django.utils.translation import gettext as _
from bot.utils import camel_to_snake

from vk_api.bot_longpoll import VkBotEventType


class Action(AbstractBase):
    """
    Base class of bot Action.

    To create new action for your bot, you should inherit from this class.

    Your action should be called 'Action<CapitalCaseActionName>' e.g. ActionPonyProfileInfo

    Params:
        action_id - generated by default
        aliases - strings which can fire your action

    Methods:
        call(self, event) - all logic of your action should be placed here
    """

    def __init__(self, aliases=None):
        self.action_id = camel_to_snake(self.__class__.__name__)
        self.aliases = aliases

    @abstractmethod
    def call(self, event):
        pass

    def __repr__(self):
        return f', '.join(self.aliases)

    def __str__(self):
        return repr(self)


class SimpleAction(Action):

    def __init__(self, notifier):
        # We need to add long_poll as ctor arg cause we're auto loading all actions
        self.notifier = notifier


class DialogAction(SimpleAction):

    def ask(self, user_id, question, answer_message=None):
        self.notifier.notify(user_id, question)
        for event in self.notifier.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if 'action' in event.object.message:
                    break
                message = event.object.message.get('text')
                if answer_message:
                    self.notifier.notify(
                        user_id,
                        answer_message.format(message)
                    )
                return message

    def choice(self, user_id, question, choices, answer_message=None):
        answer = ""
        while answer not in choices:
            answer = self.ask(
                user_id=user_id,
                question=question + ', '.join(choices),
                answer_message=answer_message
            )
            if answer in choices:
                break
            self.notifier.notify(user_id, _(
                "Такого варианта нет среди предложенных!"))
        return answer

    def __init__(self, notifier):
        super().__init__(notifier=notifier)