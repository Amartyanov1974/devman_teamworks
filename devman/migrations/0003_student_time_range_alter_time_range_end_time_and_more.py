# Generated by Django 4.0 on 2023-10-23 13:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devman', '0002_time_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='time_range',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='devman.time_range'),
        ),
        migrations.AlterField(
            model_name='time_range',
            name='end_time',
            field=models.TimeField(db_index=True, default=datetime.time(20, 0), verbose_name='Конец диапазона'),
        ),
        migrations.AlterUniqueTogether(
            name='time_range',
            unique_together={('start_time', 'end_time')},
        ),
    ]