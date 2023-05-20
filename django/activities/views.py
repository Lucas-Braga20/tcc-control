"""
Activities Views.
"""

from django.views.generic import TemplateView


class FormularyTest(TemplateView):
    """
    Formulary Test View.
    """
    template_name = 'formulary_test.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
