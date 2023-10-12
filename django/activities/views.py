"""
Implementação das Views do app de activities.

Contém as views para:
    - ActivityConfigurationListView (Listagem);
"""

from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from core.defaults import ACTIVITY_TYPES
from core.permissions import GenericPermissionMixin
from core.mixins import NotificationMixin

from activities.models import ActivityConfiguration
from activities.forms import ActivityConfigurationForm
from activities.utils import check_worked_activity, update_worked_activity


class ActivityConfigurationListView(NotificationMixin, GenericPermissionMixin, LoginRequiredMixin, TemplateView):
    """View para listagem de configurações de atividade.

    Através desta view que o professor da disciplina poderá ver
    todas as atividades.

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;

    Perfil:
        - Professor da disciplina;
    """
    template_name = 'activity-configurations/list.html'
    required_groups = ['Professor da disciplina']


class ActivityConfigurationCreateView(
    NotificationMixin,
    GenericPermissionMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
    View,
):
    """View para criação de configurações de atividade.

    Através desta view que o professor da disciplina poderá criar
    as atividades.

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;

    Perfil:
        - Professor da disciplina;
    """
    model = ActivityConfiguration
    form_class = ActivityConfigurationForm
    template_name = 'activity-configurations/editor.html'
    success_url = reverse_lazy('activities:list')
    success_message = 'Configuração de atividade criada com sucesso.'
    permission_classes = None
    authentication_classes = None
    required_groups = ['Professor da disciplina']

    def get_context_data(self, **kwargs):
        """Gera o contexto do template."""
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


class ActivityConfigurationUpdateView(
    NotificationMixin, GenericPermissionMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView,
):
    """View para atualização de configurações de atividade.

    Através desta view que o professor da disciplina poderá atualizar
    as atividades.

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;

    Perfil:
        - Professor da disciplina;
    """
    model = ActivityConfiguration
    form_class = ActivityConfigurationForm
    template_name = 'activity-configurations/editor.html'
    success_url = reverse_lazy('activities:list')
    success_message = 'Configuração de atividade atualizada com sucesso.'
    permission_classes = None
    authentication_classes = None
    required_groups = ['Professor da disciplina']

    def get_object(self, queryset=None):
        """Recupera objeto."""
        obj = super().get_object(queryset)

        if obj.archived:
            raise Http404('This activity is archived.')

        return obj

    def get_context_data(self, **kwargs):
        """Gera o contexto do template."""
        context = super().get_context_data(**kwargs)

        context['activity_already_advanced'] = check_worked_activity(self.object)

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

    def post(self, request, *args, **kwargs):
        """Atualiza a atividade."""
        response = super().post(request, *args, **kwargs)

        update_worked_activity(self.object)

        return response
