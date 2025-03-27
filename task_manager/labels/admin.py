from django.contrib import admin
from .models import Labels


@admin.register(Labels)
class LabelAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'created_at')
