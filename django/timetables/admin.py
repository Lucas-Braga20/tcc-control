"""
Admin configuration to timetables app.
"""

from django.contrib import admin

from timetables.models import Timetable, Step, StepExample


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    """
    Timetable configuration model admin.
    """
    list_display = ('id', 'description', 'teacher')


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    """
    Step configuration model admin.
    """
    list_display = ('id', 'description', 'start_date', 'send_date_advisor', 'send_date', 'presentation_date')


@admin.register(StepExample)
class StepExampleAdmin(admin.ModelAdmin):
    """
    Step Example configuration model admin.
    """
    list_display = ('id', 'file')
