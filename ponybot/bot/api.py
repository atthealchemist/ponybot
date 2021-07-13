import logging
from vk_api import VkApi, VkUpload
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.utils import get_random_id

from django.conf import settings


class BotAPI:

    def __init__(self):
        pass


class BotVkAPI(BotAPI):

    def warn(self, user_id, message, attachment=None):
        self.say(user_id, message=f"⚠ {message} ⚠", attachment=attachment)

    def say(self, user_id, message, attachment=None, prefix='', suffix=''):
        message = ' '.join([prefix, message, suffix])
        self.send_message(user_id, message, attachment)

    def congratulate(self, user_id, message, attachment=None):
        self.say(user_id, message=f"✅ {message} ✅", attachment=attachment)

    def get_conversation(self, peer_id):
        return self.api.messages.get_convesation_by_id(
            peer_ids=[peer_id],
            group_id=settings.VK_GROUP_ID
        )

    def get_user_info(self, user_id):
        return self.api.users.get(
            user_ids=[user_id],
            fields=[]
        )

    def send_message(self, receiver, message, attachment=None):
        self.api.messages.send(
            peer_id=receiver,
            message=message,
            random_id=get_random_id(),
            attachment=attachment
        )

    def upload_photo(self, photos, peer_id):
        photo = self.uploader.photo_messages(
            photos,
            peer_id=peer_id
        )

        vk_photo_url = 'photo{}_{}'.format(
            photo[0]['owner_id'], photo[0]['id']
        )

        return vk_photo_url

    def listen_new_messages(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if 'action' in event.object.message:
                    break
                self.logger.debug(f'message_new evt {event}')
                message_obj = event.object.message
                from_id = message_obj.get('from_id')
                peer_id = message_obj.get('peer_id')
                message = message_obj.get('text')
                yield from_id, peer_id, message, event

    def __init__(self):
        self.session = VkApi(
            token=settings.VK_API_TOKEN,
        )
        self.long_poll = VkBotLongPoll(self.session, settings.VK_GROUP_ID)
        self.api = self.session.get_api()
        self.uploader = VkUpload(vk=self.session)
        self.logger = logging.getLogger("Ponybot")
