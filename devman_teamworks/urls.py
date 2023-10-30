"""devman_teamworks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from devman import actions
from devman.views import ask_students_choose_time, send_group_details

urlpatterns = [
    path('', actions.redir, name='redir'),
    path('admin/', admin.site.urls),
    path('gen_stud/', actions.gen_stud, name='gen_stud'),
    path('upload_stud/', actions.upload_stud, name='upload_stud'),
    path('upload_pm/', actions.upload_pm, name='upload_pm'),
    path('gen_trello/', actions.gen_trello, name='gen_trello'),
    path('create_teamworks/', actions.create_teamworks, name='create_teamworks'),
    path('gen_discord/', actions.gen_discord, name='gen_discord'),
    path(
        'ask_students_choose_time/',
        ask_students_choose_time,
        name='ask_students_choose_time',
    ),
    path('send_group_details/', send_group_details, name='send_group_details')
]
