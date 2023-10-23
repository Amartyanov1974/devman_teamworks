from django.db import models


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

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Cтуденты'


class Project_manager(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=20)
    tg_account = models.CharField(verbose_name='Телеграм-аккаунт',
                                  max_length=20)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = 'Проект-менеджер'
        verbose_name_plural = 'Проект-менеджеры'
