from django.contrib import admin
from devman.models import Student, ProjectManager



# class StudentInline(admin.TabularInline):
    # model = Student
    # extra = 0


@admin.register(Student)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_account', 'level','far_east', 'start_time', 'end_time']


@admin.register(ProjectManager)
class Project_managerAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_account']


# @admin.register(Time_range)
# class Time_rangeAdmin(admin.ModelAdmin):
    # list_display = ['start_time', 'end_time']
    # inlines = [
        # StudentInline,
    # ]
