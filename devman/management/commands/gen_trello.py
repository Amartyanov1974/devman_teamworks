import json
from requests import request
from trello import TrelloClient

from django.core.management.base import BaseCommand
from devman.models import Student, ProjectManager, TeamWork
from django.conf import settings


def add_member(board_id, member_id):

    url = f'https://api.trello.com/1/boards/{board_id}/members/{member_id}'
    user_type = 'normal'
    query = {
      'type': user_type,
      'key': settings.TRELLO_API_KEY,
      'token': settings.TRELLO_API_TOKEN
    }

    response = request('PUT', url, params=query)
    # response.raise_for_status()


def get_member_trelloid(trello_account):

    url = f'https://api.trello.com/1/members/{trello_account}'

    headers = {
      "Accept": "application/json"
    }

    query = {
      'key': settings.TRELLO_API_KEY,
      'token': settings.TRELLO_API_TOKEN
    }

    response = request(
       "GET",
       url,
       headers=headers,
       params=query
    )
    # response.raise_for_status()
    trello_id = json.loads(response.text)['id']
    return trello_id


class Command(BaseCommand):
    def handle(self, *args, **options):
        for teamwork in TeamWork.objects.all():

            # Создание доски

            url = 'https://api.trello.com/1/boards/'
            team_students = teamwork.student.all()
            students = []
            for student in team_students:
                students.append(student.name)
            name = f'{teamwork.start_time} - {teamwork.end_time}: ПМ {teamwork.project_manager.name}, студенты: {students}'
            query = {
              'name': name,
              'key': settings.TRELLO_API_KEY,
              'token': settings.TRELLO_API_TOKEN
            }

            response = request('POST', url, params=query)
            # response.raise_for_status()
            board_id = json.loads(response.text)['id']
            trello_url = json.loads(response.text)['shortUrl']
            teamwork.trello_url = trello_url
            teamwork.save(update_fields=['trello_url'])
            for student in team_students:
                if  student.trello_account and not student.trello_id:
                    print(student.trello_account)
                    trello_id = get_member_trelloid(student.trello_account)
                    student.trello_id = trello_id
                    student.save(update_fields=['trello_id'])
                if student.trello_id:
                    add_member(board_id, student.trello_id)
            pm_trello_account = teamwork.project_manager.trello_account
            if pm_trello_account:
                print(pm_trello_account)
                trello_id = get_member_trelloid(pm_trello_account)
                add_member(board_id, trello_id)

# Выяснить что за ошибка
# Member not allowed to add a multi-board guest without allowBillableGuest parameter
