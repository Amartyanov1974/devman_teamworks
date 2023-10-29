# Generated by Django 4.0 on 2023-10-29 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devman', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='teamwork',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='students', to='devman.teamwork', verbose_name='Группа проекта'),
        ),
    ]
