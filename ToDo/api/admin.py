from django.contrib import admin
from .models import CustomUser, Task


# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'data_completed', 'completed']
    list_filter = ['user', 'data_create', 'data_completed']
    search_fields = ['user', 'title', 'tag']


