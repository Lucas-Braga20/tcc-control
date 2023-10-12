"""
Configurações de Adminsitração do app de activities.

Contém as configurações para:
    - ActivityConfigurationAdmin;
"""

from django.contrib import admin

from activities.models import ActivityConfiguration


@admin.register(ActivityConfiguration)
class ActivityConfigurationAdmin(admin.ModelAdmin):
    """Configuração de admin para configuração de atividade."""
    list_display = ('name', 'fields', 'document_insertion')
