from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Token', {'fields': (('oauth2_code'),)}),
    )
