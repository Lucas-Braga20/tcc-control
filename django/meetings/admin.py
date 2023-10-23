"""
Configurações de Adminsitração do app de meetings.

Contém as configurações para:
    - ApprovedMeetingAdmin;
    - MeetingAdmin;
"""

from django.contrib import admin

from meetings.models import Meeting, ApprovedMeeting


@admin.register(ApprovedMeeting)
class ApprovedMeetingAdmin(admin.ModelAdmin):
    """Configuração de administração para o Approved Meeting modelo."""
    list_display = ('id', 'approved', 'user', 'meeting')


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    """Configuração de administração para o Meeting modelo."""
    list_display = ('id', 'description', 'created_at', 'meeting_date', 'work_stage')
