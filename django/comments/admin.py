"""
Configurações de Adminsitração do app de comments.

Contém as configurações para:
    - CommentAdmin;
"""

from django.contrib import admin

from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Configuração de admin para comentários."""
    list_display = ('id', 'description', 'created_at', 'work_stage', 'author')
