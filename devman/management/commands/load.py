import json
import argparse
from django.core.management.base import BaseCommand
from devman.models import Student, ProjectManager, TeamWork


class Command(BaseCommand):
    def add_arguments(self, parser):
       parser.add_argument('--path', type=str, default='./people.json', help='Путь до файла')

    def handle(self, *args, **options):
        path = options['path']
        with open(path, encoding='utf-8') as json_file:
            data = json.load(json_file)

        for stud in data['students']:
            student, created = Student.objects.update_or_create(
                name=stud['name'],
                defaults={'tg_account': stud['tg_account'],
                          'trello_account': stud['trello_account'],
                          'level': stud['level'],
                          'chat_id': stud['chat_id'],
                          'trello_id': stud['trello_id']})
            print(student, created)
        for proj_manager in data['project_managers']:
            project_manager, created = ProjectManager.objects.update_or_create(
                name=proj_manager['name'],
                defaults={'tg_account': proj_manager['tg_account'],
                          'trello_account': proj_manager['trello_account'],
                          'chat_id': proj_manager['chat_id'],
                          'trello_id': proj_manager['trello_id']})
            print(project_manager, created)

        # Временная часть, создаем группу для дальнейшего создания в discord и trello
        proj_manager = ProjectManager.objects.first()
        print(proj_manager, proj_manager.tg_account, proj_manager.trello_account)
        teamwork, created = TeamWork.objects.update_or_create(
            project_manager=proj_manager)
        print(teamwork, created)
        students = Student.objects.all()[:3]
        if created:
            for student in students:
                student.teamwork = teamwork
                student. save(update_fields=['teamwork'])
                print(f'В группу {teamwork} добавили {student.name}')
