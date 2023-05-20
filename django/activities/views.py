"""
Activities Views.
"""

from typing import Any, Dict
from django.views.generic import TemplateView


class FormularyTest(TemplateView):
    """
    Formulary Test View.
    """
    template_name = 'formulary_test.html'

    def get_context_data(self, **kwargs):
        print(self.request.resolver_match)

        return super().get_context_data(**kwargs)
