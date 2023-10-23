from django.contrib import admin

from devman.models import Student, Project_manager


@admin.register(Student)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_account', 'level']
    readonly_fields = ['name', 'tg_account']

@admin.register(Project_manager)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_account']
    readonly_fields = ['name', 'tg_account']
