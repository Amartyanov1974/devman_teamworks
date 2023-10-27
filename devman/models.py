from django.db import models
from datetime import time
import asyncio

LEVEL_CHOICES = [
    ('june', 'june'),
    ('newbie+', 'newbie+'),
    ('newbie', 'newbie'),
]


class ProjectManager(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=20)
    tg_account = models.CharField(verbose_name='Телеграм-аккаунт',
                                  max_length=20)
    trello_account = models.CharField(verbose_name='Трелло-аккаунт',
                                      max_length=20)
    chat_id = models.IntegerField(verbose_name='ChatID пользователя',
                                  blank=True,
                                  null=True)
    trello_id = models.CharField(verbose_name='TrelloID пользователя',
                                 max_length=30,
                                 blank=True,
                                 null=True)
    trello_key = models.CharField(verbose_name='Trello-key',
                                 max_length=90,
                                 blank=True,
                                 null=True)
    trello_token = models.CharField(verbose_name='Trello-token',
                                 max_length=90,
                                 blank=True,
                                 null=True)


    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = 'Проект-менеджер'
        verbose_name_plural = 'Проект-менеджеры'


class TeamWork(models.Model):
    project_manager = models.OneToOneField(ProjectManager,
                                            verbose_name='Проект-менеджер',
                                            on_delete=models.SET_DEFAULT,
                                            related_name='teamwork',
                                            default=None,
                                            blank=True,
                                            null=True)

    start_time = models.TimeField(verbose_name='Начало созвона',
                                  default=time(19,00),
                                  db_index=True)
    end_time = models.TimeField(verbose_name='Окончание созвона',
                                default=time(19,20),
                                db_index=True)
    trello_url = models.URLField(verbose_name='Ссылка на доску в Trello',
                                 max_length=200,
                                 blank=True,
                                 null=True)
    discord_link = models.URLField(blank=True,
                                   null=True,
                                   verbose_name="Ссылка приглашение на дискорд сервер",
                                   max_length=200)


    def __str__(self) -> str:
        return str(f'{self.project_manager} {self.start_time} {self.end_time}')

    class Meta:
        verbose_name = 'Группа проекта'
        verbose_name_plural = 'Группы проекта'
        unique_together = [
            ['project_manager', 'start_time', 'end_time']
        ]


class Student(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=20)
    level = models.CharField(max_length=10,
                             choices=LEVEL_CHOICES,
                             verbose_name='Уровень',
                             default='newbie')
    tg_account = models.CharField(verbose_name='Телеграм-аккаунт',
                                  max_length=20)
    trello_account = models.CharField(verbose_name='Трелло-аккаунт',
                                      max_length=20,
                                      blank=True,
                                      null=True)
    far_east = models.BooleanField(verbose_name='С Дальнего Востока',
                                  default=False)
    start_time = models.TimeField(verbose_name='Начало диапазона',
                                  default=time(8,00),
                                  db_index=True)
    end_time = models.TimeField(verbose_name='Конец диапазона',
                                default=time(20,00),
                                db_index=True)
    teamwork = models.ForeignKey(TeamWork,
                                 verbose_name='Группа проекта',
                                 on_delete=models.SET_DEFAULT,
                                 related_name='student',
                                 default=None,
                                 blank=True,
                                 null=True)
    chat_id = models.IntegerField(verbose_name='ChatID пользователя',
                                  blank=True,
                                  null=True)
    trello_id = models.CharField(verbose_name='TrelloID пользователя',
                                  max_length=30,
                                  blank=True,
                                  null=True)


    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Cтуденты'
