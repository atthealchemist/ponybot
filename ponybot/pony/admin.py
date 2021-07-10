from django.contrib import admin

from .models import Pony

# Register your models here.


@admin.register(Pony)
class PonyAdmin(admin.ModelAdmin):
    readonly_fields = ('last_learning', 'last_feeding')
    list_display = (
        'name', 'sex', 'is_alive', 'owner', 'conversation',
        'satiety', 'experience', 'last_learning', 'last_feeding'
    )
    list_filter = ('is_alive', 'sex', 'owner')
