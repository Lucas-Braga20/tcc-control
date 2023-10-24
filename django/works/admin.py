"""
Configurações de Adminsitração do app de works.

Contém as configurações para:
    - FinalWorkAdmin;
    - FinalWorkStageAdmin;
    - FinalWorkVersionAdmin;
    - ChangeRequestAdmin;
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from works.models import FinalWork, FinalWorkStage, FinalWorkVersion, ChangeRequest


@admin.register(FinalWork)
class FinalWorkAdmin(admin.ModelAdmin):
    """Configuração de administração para o modelo TCC."""
    list_display = ('id', 'title', 'description', 'approved', 'supervisor', 'get_mentees', 'created_at')
    list_filter = ('supervisor', 'mentees')

    @admin.display(description=_('mentees'))
    def get_mentees(self, obj):
        """Recupera o nome dos orientandos."""
        return ', '.join([mentee.get_full_name() for mentee in obj.mentees.all()])


@admin.register(FinalWorkStage)
class FinalWorkStageAdmin(admin.ModelAdmin):
    """Configuração de administração para o modelo Etapa de TCC."""
    list_display = ('id', 'presented', 'status', 'final_work')


@admin.register(FinalWorkVersion)
class FinalWorkVersionAdmin(admin.ModelAdmin):
    """Configuração de administração para o modelo Versão de Etapa de TCC."""
    list_display = ('id', 'created_at', 'content', 'work_stage')


@admin.register(ChangeRequest)
class ChangeRequestAdmin(admin.ModelAdmin):
    """Configuração de administração para o modelo Pedido de mudança de TCC."""
    list_display = ('id', 'approved', 'description', 'created_at', 'requester', 'work_stage')
