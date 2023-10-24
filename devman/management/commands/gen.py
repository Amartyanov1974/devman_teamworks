import argparse
from datetime import time
from random import randint, choice
from django.core.management.base import BaseCommand
from devman.models import Student


LEVEL_CHOICES = ['June', 'newbie+', 'newbie']


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=50, help='Количество сгенерированных студентов')

    def handle(self, *args, **options):

        count = options['count']

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
