"""
Admin configuration to comments app.
"""

from django.contrib import admin

from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Comment configuration model admin.
    """
    list_display = ('id', 'description', 'created_at', 'work_step', 'author')
