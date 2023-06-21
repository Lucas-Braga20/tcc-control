"""
Works views.
"""

from django.views.generic import TemplateView


class WorkStageView(TemplateView):
    """
    Work Stage screen.
    """
    template_name = 'final-work-stages/stages.html'
