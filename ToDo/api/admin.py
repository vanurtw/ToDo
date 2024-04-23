from django.contrib import admin
from .models import CustomUser


# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmib(admin.ModelAdmin):
    fields = ('__all__',)
