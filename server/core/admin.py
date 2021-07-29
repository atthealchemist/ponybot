from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Pony, PonybotUser


@admin.register(Pony)
class PonyAdmin(admin.ModelAdmin):
    readonly_fields = ("last_learning", "last_feeding")
    list_display = (
        "name",
        "race",
        "is_alive",
        "owner",
        "conversation",
        "satiety",
        "experience",
        "last_learning",
        "last_feeding",
    )
    list_filter = ("is_alive", "race", "owner")


@admin.register(PonybotUser)
class PonybotUserAdmin(ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "is_superuser",
        "is_subscriber",
    )
    list_filter = ("is_superuser", "is_subscriber")
