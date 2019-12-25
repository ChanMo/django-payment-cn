from django.contrib import admin

from .models import *


class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'method', 'action', 'description', 'amount', 'number', 'openid', 'is_success', 'error_msg', 'created', 'updated')
    list_filter = ('method', 'action', 'is_success', 'created', 'updated')
    list_per_page = 12
    search_fields = ('user__username',)
    raw_id_fields = ('user',)


admin.site.register(Log, LogAdmin)
