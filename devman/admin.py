from django.contrib import admin
from devman.models import Student, ProjectManager, TeamWork
from django.core.management import call_command


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_account', 'level','far_east', 'start_time', 'end_time']
    change_list_template = "admin/stud_change_list.html"


@admin.register(ProjectManager)
class ProjectManagerAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_account']
    change_list_template = "admin/pm_change_list.html"


@admin.register(TeamWork)
class TeamWorkAdmin(admin.ModelAdmin):
    list_display = ['project_manager', 'start_time', 'end_time']
    inlines = [
        StudentInline,
    ]
    actions = ['run_custom_command']
    change_list_template = "admin/teamwork_change_list.html"

    def run_custom_command(self, request, queryset):
        call_command('discord')
        self.message_user(request, 'Команда успешно выполнена')

    run_custom_command.short_description = 'Генерация групп в дискорд сервере'
