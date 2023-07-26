"""
Admin configuration to Mettings App.
"""

from django.contrib import admin

from meetings.models import Meeting, ApprovedMeeting


@admin.register(ApprovedMeeting)
class ApprovedMeetingAdmin(admin.ModelAdmin):
    """
    Approved Meeting configuration model admin.
    """
    list_display = ('id', 'approved', 'user', 'meeting')


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    """
    Meeting configuration model admin.
    """
    list_display = ('id', 'description', 'created_at', 'meeting_date', 'work_stage')
