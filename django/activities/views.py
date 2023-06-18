"""
Activities Views.
"""

from django.views.generic import TemplateView

from core.defaults import ACTIVITY_TYPES

from activities.models import ActivityConfiguration
from activities.forms import ActivityConfigurationForm


class ActivityConfigurationListView(TemplateView):
    """
    Activity configuration list screen.
    """
    template_name = 'activity-configurations/list.html'


class ActivityConfigurationCreateView(TemplateView):
    """
    Activity configuration create screen.
    """
    template_name = 'activity-configurations/editor.html'
    model = ActivityConfiguration
    form = ActivityConfigurationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        types = []
        for type in ACTIVITY_TYPES:
            if type == 'text':
                types.append({
                    'value': type,
                    'label': 'Texto'
                })

            if type == 'number':
                types.append({
                    'value': type,
                    'label': 'Número'
                })

            if type == 'rich':
                types.append({
                    'value': type,
                    'label': 'Editor'
                })

        context['types'] = types

        return context


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
