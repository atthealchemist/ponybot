from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from .models import PonybotUser


# Register your models here.
@admin.register(PonybotUser)
class PonybotUserAdmin(ModelAdmin):
    list_display = ('username', 'first_name', 'last_name',
                    'is_superuser', 'is_subscriber')
    list_filter = ('is_superuser', 'is_subscriber')