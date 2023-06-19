"""
Activities Views.
"""

from django.views.generic import TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404

from core.defaults import ACTIVITY_TYPES

from activities.models import ActivityConfiguration
from activities.forms import ActivityConfigurationForm


class ActivityConfigurationListView(TemplateView):
    """
    Activity configuration list screen.
    """
    template_name = 'activity-configurations/list.html'


@method_decorator(csrf_exempt, name='dispatch')
class ActivityConfigurationCreateView(SuccessMessageMixin, CreateView):
    """
    Activity configuration create screen.
    """
    template_name = 'activity-configurations/editor.html'
    model = ActivityConfiguration
    form_class = ActivityConfigurationForm
    success_url = reverse_lazy('activities:list')
    success_message = 'Configuração de atividade criada com sucesso.'
    permission_classes = None
    authentication_classes = None

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


@method_decorator(csrf_exempt, name='dispatch')
class ActivityConfigurationUpdateView(SuccessMessageMixin, UpdateView):
    """
    Activity configuration update screen.
    """
    template_name = 'activity-configurations/editor.html'
    model = ActivityConfiguration
    form_class = ActivityConfigurationForm
    success_url = reverse_lazy('activities:list')
    success_message = 'Configuração de atividade atualizada com sucesso.'
    permission_classes = None
    authentication_classes = None

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.archived:
            raise Http404('This activity is archived.')

        return obj

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
