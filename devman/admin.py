from django.contrib import admin
from devman.models import Student, Project_manager, Time_range



class StudentInline(admin.TabularInline):
    model = Student
    extra = 0


@admin.register(Student)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_account', 'level','far_east', 'time_range']


@admin.register(Project_manager)
class Project_managerAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_account']


@admin.register(Time_range)
class Time_rangeAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time']
    inlines = [
        StudentInline,
    ]
