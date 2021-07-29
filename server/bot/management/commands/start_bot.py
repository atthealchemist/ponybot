
from django.core.management.base import BaseCommand, CommandError
from bot.service import BotService as PonybotService


class Command(BaseCommand):
    help = 'Starts vk bot'

    def handle(self, *args, **options):
        bot = PonybotService()
        bot.start()
