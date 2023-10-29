from django.contrib import admin
from devman.models import Student, ProjectManager, TeamWork
from django.core.management import call_command


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class TeamWorkInline(admin.TabularInline):
    model = TeamWork
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_account', 'level','far_east', 'start_time', 'end_time']
    change_list_template = "admin/stud_change_list.html"
    readonly_fields = ['chat_id', 'trello_id', ]
    ordering = ('name',)


@admin.register(ProjectManager)
class ProjectManagerAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_account']
    inlines = [
        TeamWorkInline,
    ]
    change_list_template = "admin/pm_change_list.html"
    readonly_fields = ['chat_id', 'trello_key', 'trello_id', 'trello_token']
    ordering = ('name',)


@admin.register(TeamWork)
class TeamWorkAdmin(admin.ModelAdmin):
    list_display = ['project_manager', 'number_students', 'start_time', 'end_time', 'trello_url', 'discord_link']
    inlines = [
        StudentInline,
    ]
    readonly_fields = ['trello_url', 'discord_link']
    actions = ['run_custom_command']
    change_list_template = "admin/teamwork_change_list.html"
    ordering = ('start_time',)

    def run_custom_command(self, request, queryset):
        call_command('discord')
        self.message_user(request, 'Команда успешно выполнена')

    run_custom_command.short_description = 'Генерация групп в дискорд сервере'
