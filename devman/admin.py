from django.contrib import admin
from devman.models import Student, Project_manager, Time_range


@admin.register(Student)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_account', 'level']
    readonly_fields = ['name', 'tg_account']


@admin.register(Project_manager)
class Project_managerAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_account']
    readonly_fields = ['name', 'tg_account']


@admin.register(Time_range)
class Time_rangeAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time']

