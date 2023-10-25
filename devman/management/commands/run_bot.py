from django.core.management import BaseCommand
from django.conf import settings
from telegram.ext import Updater


def main():
    tg_bot_token = settings.TG_BOT_TOKEN
    updater = Updater(token=tg_bot_token)
    dispatcher = updater.dispatcher

    updater.start_polling()
    updater.idle()


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()