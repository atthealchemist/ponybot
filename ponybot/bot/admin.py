from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import PonybotUser


@admin.register(PonybotUser)
class PonybotAdmin(ModelAdmin):
    list_display = ('username', 'is_superuser', 'is_subscriber')
    list_filter = ('is_superuser', 'is_subscriber')
