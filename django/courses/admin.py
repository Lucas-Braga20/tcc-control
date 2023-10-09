"""Configuração de administração para o módulo Courses."""

from django.contrib import admin

from courses.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Configuração para Course."""
    list_display = ('id', 'description', 'archived')