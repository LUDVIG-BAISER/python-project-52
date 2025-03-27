from django.contrib import admin
from .models import Statuses


@admin.register(Statuses)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'created_at')
