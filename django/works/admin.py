"""
Admin configuration to works app.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from works.models import FinalWork, FinalWorkStage, FinalWorkVersion, ChangeRequest


@admin.register(FinalWork)
class FinalWorkAdmin(admin.ModelAdmin):
    """
    Final work configuration model admin.
    """
    list_display = ('id', 'description', 'approved', 'supervisor', 'get_mentees')
    list_filter = ('supervisor', 'mentees')

    @admin.display(description=_('mentees'))
    def get_mentees(self, obj):
        """
        Method to return mentees names.
        """
        return ', '.join([mentee.get_full_name() for mentee in obj.mentees.all()])


@admin.register(FinalWorkStage)
class FinalWorkStageAdmin(admin.ModelAdmin):
    """
    Final work stage configuration model admin.
    """
    list_display = ('id', 'presented', 'status', 'final_work')


@admin.register(FinalWorkVersion)
class FinalWorkVersionAdmin(admin.ModelAdmin):
    """
    Final work version configuration model admin.
    """
    list_display = ('id', 'created_at', 'content', 'work_stage')


@admin.register(ChangeRequest)
class ChangeRequestAdmin(admin.ModelAdmin):
    """
    Change Request configuration model admin.
    """
    list_display = ('id', 'approved', 'description', 'created_at', 'requester', 'work_stage')
