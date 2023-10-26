import json
from requests import request
from trello import TrelloClient

from django.core.management.base import BaseCommand
from devman.models import Student, ProjectManager, TeamWork
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        for teamwork in TeamWork.objects.all():

            # Создание доски

            url = 'https://api.trello.com/1/boards/'
            students = []
            for student in teamwork.student.all():
                students.append(student.name)

            name = f'{teamwork.start_time} - {teamwork.end_time}: ПМ {teamwork.project_manager.name}, студенты: {students}'
            query = {
              'name': name,
              'key': settings.TRELLO_API_KEY,
              'token': settings.TRELLO_API_TOKEN
            }

            response = request('POST', url, params=query)
            trello_url = json.loads(response.text)['shortUrl']
            print(trello_url)
            teamwork.trello_url = trello_url
            teamwork. save(update_fields=['trello_url'])
