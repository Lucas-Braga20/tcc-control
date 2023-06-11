"""
Admin configuration to users app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    User configuration model admin.
    """
    list_display = ('username', 'name', 'email', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (_('Account'), {'fields': ('username', 'password')}),
        (_('Personal'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Internal Configuration'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Permissions'), {'fields': ('groups', 'user_permissions')}),
    )

    @admin.display(description=_('name'))
    def name(self, obj):
        """
        Method to return user full name.
        """
        return obj.get_full_name()
