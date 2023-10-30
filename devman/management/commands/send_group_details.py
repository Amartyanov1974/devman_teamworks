from django.conf import settings
from django.core.management import BaseCommand
from telegram import Bot
from telegram.error import BadRequest

from devman.models import Student


def main():
    tg_bot_token = settings.TG_BOT_TOKEN
    bot = Bot(token=tg_bot_token)

    students = Student.objects.all()

    template = (
        'Созвоны по вашему проекту будут с {start_time} до {end_time}.\n'
        'Ваша ссылка на трелло {trello_url}.\n'
        'Ваша ссылка на дискорд {discord_url}'
    )

    for student in students:
        if student.teamwork:
            teamwork = student.teamwork
            start_time = teamwork.start_time.strftime("%H:%M")
            end_time = teamwork.end_time.strftime("%H:%M")
            trello_url = teamwork.trello_url
            discord_url = teamwork.discord_link
            message = template.format(
                start_time=start_time,
                end_time=end_time,
                trello_url=trello_url,
                discord_url=discord_url,
            )
            if student.chat_id:
                try:
                    bot.send_message(student.chat_id, text=message)
                except BadRequest as e:
                    pass


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()
