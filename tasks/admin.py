from django.contrib import admin
from.models import Task

class TaskAdmin(admin.ModelAdmin):#De esta forma permite ver los campos de solo lectura en el panel de admin
    readonly_fields = ("date_created", )

# Register your models here.
admin.site.register(Task, TaskAdmin)#Recordar pasar la clase