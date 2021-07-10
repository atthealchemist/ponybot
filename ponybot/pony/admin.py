from django.contrib import admin

from .models import Pony

# Register your models here.


@admin.register
class PonyAdmin(admin.ModelAdmin):
    list_display = "__all__"
