from django.conf import settings
from django.core.management import BaseCommand
from telegram import Bot

from devman.models import Student


def main():
    tg_bot_token = settings.TG_BOT_TOKEN
    bot = Bot(token=tg_bot_token)

    students = Student.objects.all()

    message = (
        'Вы добавлены в список студентов участвующих в командном проекте'
        ' на следующей неделе.\n'
        'Пожалуйста нажмите /start для внесения информации о ваших '
        'временных возможностях.'
    )

    for student in students:
        if student.chat_id:
            bot.send_message(student.chat_id, text=message)


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()
