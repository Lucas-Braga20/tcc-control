"""
Admin configuration to timetables app.
"""

from django.contrib import admin

from timetables.models import Timetable, Stage, StageExample


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    """
    Timetable configuration model admin.
    """
    list_display = ('id', 'description', 'teacher', 'get_participants')

    def get_participants(self, obj):
        return ', '.join([participant.get_full_name() for participant in obj.participants.all()])


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    """
    Stage configuration model admin.
    """
    list_display = ('id', 'description', 'start_date', 'send_date_supervisor', 'send_date', 'presentation_date')


@admin.register(StageExample)
class StageExampleAdmin(admin.ModelAdmin):
    """
    Stage example configuration model admin.
    """
    list_display = ('id', 'file')
