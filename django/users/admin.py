"""
Configurações de Adminsitração do app de users.

Contém as configurações para:
    - UserAdmin;
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Configuração de administração para o Usuário modelo."""
    list_display = ('username', 'name', 'email', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (_('Account'), {'fields': ('username', 'password')}),
        (_('Personal'), {'fields': ('first_name', 'last_name', 'email', 'rgm')}),
        (_('Internal Configuration'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Permissions'), {'fields': ('groups', 'user_permissions')}),
    )

    @admin.display(description=_('name'))
    def name(self, obj):
        """Recupera o nome completo do usuário."""
        return obj.get_full_name()
