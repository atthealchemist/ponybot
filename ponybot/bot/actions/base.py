from abc import ABC as AbstractBase, abstractmethod

from django.utils.translation import gettext as _
from bot.utils import camel_to_snake

from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotEventType


import requests


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


class UploadPhotoAction(SimpleAction):

    def __get_attachments(self, event):
        res = []
        attachments = event.object.message.get('attachments')
        for attach in attachments:
            res.extend([
                s for s in attach.get('photo').get('sizes')
                if s.get('type') == 'z'
            ])
        return res

    def ask_photo(self, user_id, question):
        self.notifier.notify(user_id, question)
        for event in self.notifier.long_poll.listen():
            if event.type == VkBotEventType.PHOTO_NEW:
                print('photo_event', event)
            if event.type == VkBotEventType.MESSAGE_NEW:
                if 'action' in event.object.message:
                    break

                # We're getting attachment url from event
                for attachment in self.__get_attachments(event):
                    with requests.Session() as session:
                        image = session.get(attachment.get('url'), stream=True)
                        photo_url = self.attach(
                            image.raw,
                            peer_id=user_id
                        )
                        return photo_url

    def attach(self, photo_path, peer_id=-1):
        upload = VkUpload(vk=self.notifier.session)

        photo = upload.photo_messages(
            photo_path,
            peer_id=peer_id
        )

        vk_photo_url = 'photo{}_{}'.format(
            photo[0]['owner_id'], photo[0]['id']
        )

        return vk_photo_url

    def __init__(self, notifier):
        super().__init__(notifier=notifier)
