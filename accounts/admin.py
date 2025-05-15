from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserAccount


class ProfileInline(admin.StackedInline):

    model = UserAccount
    can_delete = False


class UserAccountAdmin(BaseUserAdmin):

    inlines = [
        ProfileInline,
    ]


admin.site.unregister(User)
admin.site.register(User, UserAccountAdmin)
