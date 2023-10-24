from django.db import models
from datetime import time


LEVEL_CHOICES = [
    ('June', 'June'),
    ('newbie+', 'newbie+'),
    ('newbie', 'newbie'),
]


class Student(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=20)
    level = models.CharField(max_length=10,
                             choices=LEVEL_CHOICES,
                             verbose_name='Уровень',
                             default='newbie')
    tg_account = models.CharField(verbose_name='Телеграм-аккаунт',
                                  max_length=20)
    # time_range = models.ForeignKey(Time_range,
                                   # on_delete = models.SET_DEFAULT,
                                   # related_name='students',
                                   # null=True,
                                   # blank=True,
                                   # default=None)
    far_east = models.BooleanField(verbose_name='С Дальнего Востока',
                                  default=False)
    start_time = models.TimeField(verbose_name='Начало диапазона',
                                 default=time(8,00),
                                 db_index=True)
    end_time = models.TimeField(verbose_name='Конец диапазона',
                                 default=time(20,00),
                                 db_index=True)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Cтуденты'


class ProjectManager(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=20)
    tg_account = models.CharField(verbose_name='Телеграм-аккаунт',
                                  max_length=20)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = 'Проект-менеджер'
        verbose_name_plural = 'Проект-менеджеры'
