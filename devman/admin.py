from django.contrib import admin
from devman.models import Student, ProjectManager, TeamWork



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
