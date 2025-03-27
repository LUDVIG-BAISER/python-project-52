from django.contrib import admin

# Register your models here.
from .models import Users


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_display = ('id', 'first_name', 'last_name', 'username', 'password')

# admin.site.register(Users, UserAdmin)
