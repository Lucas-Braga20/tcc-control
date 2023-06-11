"""
Admin configuration to works app.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from works.models import TCCWork, WorkStep, WorkStepVersion, ChangeRequest, Comment


@admin.register(TCCWork)
class TCCWorkAdmin(admin.ModelAdmin):
    """
    TCC Work configuration model admin.
    """
    list_display = ('id', 'description', 'approved', 'advisor', 'advised')
    list_filter = ('approved', 'advisor')

    @admin.display(description=_('advised'))
    def advised(self, obj):
        """
        Method to return advised names.
        """
        return [advised.get_full_name() for advised in obj.advised.all()].join(', ')


@admin.register(WorkStep)
class WorkStepAdmin(admin.ModelAdmin):
    """
    Work Step configuration model admin.
    """
    list_display = ('id', 'presented', 'status')


@admin.register(WorkStepVersion)
class WorkStepVersionAdmin(admin.ModelAdmin):
    """
    Work Step Version configuration model admin.
    """
    list_display = ('id', 'created_at', 'content')


@admin.register(ChangeRequest)
class ChangeRequestAdmin(admin.ModelAdmin):
    """
    Change Request configuration model admin.
    """
    list_display = ('id', 'approved', 'description', 'created_at', 'requester')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Comment configuration model admin.
    """
    list_display = ('id', 'description', 'created_at', 'work_step', 'author')
