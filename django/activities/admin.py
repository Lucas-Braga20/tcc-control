"""
Admin configuration to activities app.
"""

from django.contrib import admin

from activities.models import ActivityConfiguration


@admin.register(ActivityConfiguration)
class ActivityConfigurationAdmin(admin.ModelAdmin):
    """
    Activity configuration model admin.
    """
    list_display = ('name', 'fields', 'document_insertion')
