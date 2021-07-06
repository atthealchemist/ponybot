
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from ponybot.service import PonybotService


class Command(BaseCommand):
    help = 'Starts vk bot'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        bot = PonybotService(
            token=settings.VK_API_TOKEN,
            group_id=settings.VK_GROUP_ID
        )
        bot.start()
