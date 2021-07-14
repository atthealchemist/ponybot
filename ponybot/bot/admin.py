from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import PonybotAction, PonybotUser, DialogSession


@admin.register(PonybotUser)
class PonybotUserAdmin(ModelAdmin):
    list_display = ('username', 'first_name', 'last_name',
                    'is_superuser', 'is_subscriber')
    list_filter = ('is_superuser', 'is_subscriber')


@admin.register(PonybotAction)
class PonybotActionAdmin(ModelAdmin):
    list_display = ('name', 'action_aliases', 'is_admin_only')
    list_filter = ('is_admin_only',)

    def action_aliases(self, action):
        return ', '.join(action.aliases)


@admin.register(DialogSession)
class DialogSessionAdmin(ModelAdmin):
    list_display = ('user_id', 'peer_id', 'action_id',
                    'opened', 'last_message')
    list_filter = ('opened',)
