import argparse
from datetime import time, timedelta, datetime, date
from random import randint, choice
from django.core.management.base import BaseCommand
from testdb.models import Student
import pandas as pd
import numpy as np

LEVEL_CHOICES = ['June', 'newbie+', 'newbie']


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=50, help='Количество сгенерированных студентов')

    def handle(self, *args, **options):

        count = options['count']

        students = []

        for student in Student.objects.all():
            students.append([student.name,
                             student.start_time,
                             student.end_time,
                             datetime.combine(date.min, student.end_time)-datetime.combine(date.min, student.start_time),
                             ])

        df = pd.DataFrame(students, columns=['name', 'start_time', 'end_time', 'delta_time'])
        print(df.sort_values(by = ['delta_time', 'start_time']).head(1)['start_time'])


