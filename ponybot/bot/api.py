import logging
from django.contrib.auth import get_user_model
from vk_api import VkApi, VkUpload
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.utils import get_random_id

from django.conf import settings


class BotAPI:

    def __init__(self):
        pass


class BotVkAPI(BotAPI):

    def warn(self, session, message, attachment=None):
        self.say(
            session,
            prefix='⚠',
            suffix='⚠',
            message=message, attachment=attachment
        )

    def say(self, session, message, attachment=None, prefix='', suffix='', no_alloc=False):
        user = get_user_model().objects.get(username=session.user_id)
        alloc = f"{user.first_name} {user.last_name}"

        content = f"{alloc}, {message[:1].lower() + message[1:]}"
        if no_alloc:
            content = message

        message = ' '.join([prefix, content, suffix])
        self.send_message(session.peer_id, message=message,
                          attachment=attachment)

    def congratulate(self, session, message, attachment=None):
        self.say(session, message=f"✅ {message} ✅", attachment=attachment)

    def get_conversation_title(self, peer_id):
        return self.api.messages.get_conversations_by_id(
            peer_ids=[peer_id],
            group_id=settings.VK_GROUP_ID
        ).get('items')[0].get('chat_settings').get('title')

    def get_user_name(self, user_id):
        user_info = self.api.users.get(
            user_ids=[user_id],
            fields=[]
        )[0]
        return f"{user_info.get('first_name')} {user_info.get('last_name')}"

    def send_message(self, receiver, message, attachment=None):
        self.api.messages.send(
            peer_id=receiver,
            message=message,
            random_id=get_random_id(),
            attachment=attachment,
            disable_mentions=True
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
