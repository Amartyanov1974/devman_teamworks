from django.contrib import admin
from devman.models import Student, ProjectManager, TeamWork
from django.core.management import call_command


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0


@admin.register(Student)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_account', 'level','far_east', 'start_time', 'end_time']


@admin.register(ProjectManager)
class ProjectManagerAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_account']


@admin.register(TeamWork)
class TeamWorkAdmin(admin.ModelAdmin):
    list_display = ['project_manager', 'start_time', 'end_time']
    inlines = [
        StudentInline,
    ]
    actions = ['run_custom_command']

    def run_custom_command(self, request, queryset):
        call_command('discord')
        self.message_user(request, 'Команда успешно выполнена')

    run_custom_command.short_description = 'Генерация групп в дискорд сервере'

