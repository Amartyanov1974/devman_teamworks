import json
from datetime import time
from random import randint, choice
import logging
import requests
from trello import TrelloClient
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.management import call_command

from devman.models import Student, ProjectManager, TeamWork
from devman.forms import UploadFileForm


LEVEL_CHOICES = ['june', 'newbie+', 'newbie']


def gen_stud(request):
    count = 50
    for number in range(count):
        name = f'student{number}'
        tg_account = f'@{name}'
        level=choice(LEVEL_CHOICES)
        start_time = randint(9, 19)
        end_time = randint(start_time + 1, 21)
        start_time = time(start_time, 0)
        end_time = time(end_time, 0)
        student, created = Student.objects.update_or_create(
            name=name,
            defaults={'level': level, 'tg_account': tg_account,
                      'start_time': start_time, 'end_time': end_time})
    return redirect('/admin/devman/student/')


def save_students(json_file):
    data = json.load(json_file)

    for stud in data['students']:
        student, created = Student.objects.update_or_create(
            name=stud['name'],
            defaults={'tg_account': stud['tg_account'],
                      'trello_account': stud['trello_account'],
                      'level': stud['level'],
                      'chat_id': stud['chat_id'],
                      'trello_id': stud['trello_id']})


def save_pm(json_file):
    data = json.load(json_file)
    for proj_manager in data['project_managers']:
        project_manager, created = ProjectManager.objects.update_or_create(
            name=proj_manager['name'],
            defaults={'tg_account': proj_manager['tg_account'],
                      'trello_account': proj_manager['trello_account'],
                      'chat_id': proj_manager['chat_id'],
                      'trello_id': proj_manager['trello_id'],
                      'trello_key': proj_manager['trello_key'],
                      'trello_token': proj_manager['trello_token']})
        print(project_manager, created)


def upload_stud(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        try:
        #if form.is_valid():
            save_students(request.FILES['file'])
            return redirect('/admin/devman/student/')
        except Exception as e:
            logging.error(str(e))
    else:
        form = UploadFileForm(request.POST, request.FILES)
    return render(request, 'upload.html', {'form': form})


def upload_pm(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        try:
        #if form.is_valid():
            save_pm(request.FILES['file'])
            return redirect('/admin/devman/projectmanager/')
        except Exception as e:
            logging.error(str(e))
    else:
        form = UploadFileForm(request.POST, request.FILES)
    return render(request, 'upload.html', {'form': form})


def create_teamworks(request):
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
    return redirect('/admin/devman/teamwork/')


def add_member(board_id, member_id, trello_api_key, trello_api_token):

    url = f'https://api.trello.com/1/boards/{board_id}/members/{member_id}'
    user_type = 'normal'
    query = {
      'type': user_type,
      'key': trello_api_key,
      'token': trello_api_token
    }

    response = requests.request('PUT', url, params=query)
    # response.raise_for_status()


def get_member_trelloid(trello_account, trello_api_key, trello_api_token):

    url = f'https://api.trello.com/1/members/{trello_account}'

    headers = {
      "Accept": "application/json"
    }

    query = {
      'key': trello_api_key,
      'token': trello_api_token
    }

    response = requests.request(
       "GET",
       url,
       headers=headers,
       params=query
    )
    # response.raise_for_status()
    trello_id = json.loads(response.text)['id']
    return trello_id


def gen_trello(request):
    for teamwork in TeamWork.objects.all():

        # Создание доски

        url = 'https://api.trello.com/1/boards/'
        team_students = teamwork.student.all()
        students = []
        for student in team_students:
            students.append(student.name)
        name = f'{teamwork.start_time} - {teamwork.end_time}: ПМ {teamwork.project_manager.name}, студенты: {students}'
        trello_api_key = teamwork.project_manager.trello_key
        trello_api_token = teamwork.project_manager.trello_token
        query = {
            'name': name,
            'key': trello_api_key,
            'token': trello_api_token
        }

        response = requests.request('POST', url, params=query)
        # response.raise_for_status()
        board_id = json.loads(response.text)['id']
        trello_url = json.loads(response.text)['shortUrl']
        teamwork.trello_url = trello_url
        teamwork.save(update_fields=['trello_url'])
        for student in team_students:
            if  student.trello_account and not student.trello_id:
                print(student.trello_account)
                trello_id = get_member_trelloid(student.trello_account, trello_api_key, trello_api_token)
                student.trello_id = trello_id
                student.save(update_fields=['trello_id'])
            if student.trello_id:
                print(board_id, student.trello_id, trello_api_key, trello_api_token)
                add_member(board_id, student.trello_id, trello_api_key, trello_api_token)
        # pm_trello_account = teamwork.project_manager.trello_account
        # if pm_trello_account:
            # print(pm_trello_account)
            # trello_id = get_member_trelloid(pm_trello_account)
            # add_member(board_id, trello_id)
    return redirect('/admin/devman/teamwork/')


def gen_discord(request):
    call_command('discord')
    return redirect('/admin/devman/teamwork/')
