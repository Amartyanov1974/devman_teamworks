from django.contrib import admin
from devman.models import Student, ProjectManager, TeamWork, TeamWorkCalculation
from django.core.management import call_command


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

class StudentCalculationInline(admin.TabularInline):
    model = TeamWorkCalculation.students_candidate.through

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
    list_display = ['name', 'teamwork', 'tg_account', 'level', 'start_time', 'end_time', 'far_east']
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

    change_list_template = "admin/teamwork_change_list.html"
    ordering = ('start_time',)


@admin.register(TeamWorkCalculation)
class TeamWorkCalculationAdmin(admin.ModelAdmin):
    list_display = ['project_manager', 'number_students', 'start_time', 'end_time']
    inlines = [
        StudentCalculationInline,
    ]
    ordering = ('start_time',)
