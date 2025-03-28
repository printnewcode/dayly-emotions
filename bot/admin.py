from django.contrib import admin
from .models import (
    User,
    DaylyWriting
)


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'user_id']
    list_display_links = ['username']
    search_fields = ['username', 'user_id', ]
    ordering = ['user_id', ]
class DaylyWritingAdmin(admin.ModelAdmin):
    list_display = ['day', 'user']
    list_display_links = ['day']




admin.site.register(DaylyWriting, DaylyWritingAdmin)
admin.site.register(User, UserAdmin)
