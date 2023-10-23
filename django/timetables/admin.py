"""
Configurações de Adminsitração do app de timetables.

Contém as configurações para:
    - TimetableAdmin;
    - StageAdmin;
    - StageExampleAdmin;
"""

from django.contrib import admin

from timetables.models import Timetable, Stage, StageExample


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    """Configuração de administração para o Timetable modelo."""
    list_display = ('id', 'description', 'teacher', 'get_participants')

    def get_participants(self, obj):
        return ', '.join([participant.get_full_name() for participant in obj.participants.all()])


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    """Configuração de administração para o Stage modelo."""
    list_display = ('id', 'description', 'start_date', 'send_date_supervisor', 'send_date', 'presentation_date')


@admin.register(StageExample)
class StageExampleAdmin(admin.ModelAdmin):
    """Configuração de administração para o StageExample modelo."""
    list_display = ('id', 'file')
