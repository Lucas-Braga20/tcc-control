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

    def post(self, request, *args, **kwargs):
        """
        Post method.
        """

        body = request.POST
        print(body)

        return self.render_to_response()
