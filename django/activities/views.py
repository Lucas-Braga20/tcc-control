"""
Activities Views.
"""

from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from core.defaults import ACTIVITY_TYPES

from activities.models import ActivityConfiguration
from activities.forms import ActivityConfigurationForm

from core.permissions import GenericPermissionMixin


class ActivityConfigurationListView(GenericPermissionMixin, LoginRequiredMixin, TemplateView):
    """
    Activity configuration list screen.
    """
    template_name = 'activity-configurations/list.html'
    required_groups = ['Professor da disciplina']


class ActivityConfigurationCreateView(GenericPermissionMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView, View):
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
    required_groups = ['Professor da disciplina']

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


class ActivityConfigurationUpdateView(GenericPermissionMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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
    required_groups = ['Professor da disciplina']

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
