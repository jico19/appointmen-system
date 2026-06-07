from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'phone_no', 'first_name', 'last_name']
    
    fieldsets = (
        ("BASIC_INFO", {
            'fields': ('username', 'password')
        }),
        ("PERSONAL_INFO", {
            'fields': ('first_name', 'last_name', 'email', 'phone_no', 'role')
        }),
    )
