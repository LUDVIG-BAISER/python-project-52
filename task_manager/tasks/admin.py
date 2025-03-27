from django.contrib import admin
from .models import Tasks


@admin.register(Tasks)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'author', 'created_at')
