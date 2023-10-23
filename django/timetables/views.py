"""
Implementação das Views do app de timetables.

Contém as views para:
    - TimetableListView (Listagem);
    - TimetableCreateView (Create);
    - TimetableUpdateView (Atualização);
    - TimetableStageCalendarView (Calendário);
    - TimetableDetailView (Detalhes);
"""

from django.views.generic import CreateView, TemplateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from timetables.models import Timetable, Stage
from timetables.forms import TimetableForm

from core.permissions import GenericPermissionMixin, UserGroup
from core.mixins import NotificationMixin


class TimetableListView(
    NotificationMixin, GenericPermissionMixin, LoginRequiredMixin, TemplateView,
):
    """View para listagem de cronogramas.

    Através desta view que o professor da disciplina poderá ver
    todas os cronogramas que ele é criador.

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;

    Perfil:
        - Professor da disciplina;
    """
    template_name = 'timetables/list.html'
    required_groups = ['Professor da disciplina']


class TimetableCreateView(
    NotificationMixin, GenericPermissionMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView,
):
    """View para listagem de cronogramas.

    Através desta view que o professor da disciplina poderá criar
    um cronograma.

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;

    Perfil:
        - Professor da disciplina;
    """
    template_name = 'timetables/editor.html'
    model = Timetable
    form_class = TimetableForm
    success_url = reverse_lazy('timetables:list')
    success_message = 'Cronograma criado com sucesso.'
    permission_classes = None
    authentication_classes = None
    required_groups = ['Professor da disciplina']

    def get_initial(self):
        """Seta os valores iniciais do formulário."""
        initial = super().get_initial()
        initial['teacher'] = self.request.user
        return initial

    def get_form_kwargs(self):
        """Recupera os argumentos do formulário."""
        kwargs = super().get_form_kwargs()

        kwargs.update({'is_creation': True})

        return kwargs


class TimetableUpdateView(
    NotificationMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView,
):
    """View para atualização de cronogramas.

    Através desta view que o professor da disciplina poderá atualizar
    um cronograma.

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;

    Perfil:
        - Professor da disciplina;
    """
    template_name = 'timetables/editor.html'
    model = Timetable
    form_class = TimetableForm
    success_url = reverse_lazy('timetables:list')
    success_message = 'Cronograma atualizado com sucesso.'
    permission_classes = None
    authentication_classes = None

    def get_context_data(self, **kwargs):
        """Gera o contexto do template."""
        context = super().get_context_data(**kwargs)

        timetable = self.get_object()

        context['mentees'] = timetable.participants.filter(
            groups__name='Orientando',
        ).values_list('id', flat=True)

        context['supervisors'] = timetable.participants.filter(
            groups__name='Orientador',
        ).values_list('id', flat=True)

        return context


class TimetableStageCalendarView(
    NotificationMixin, LoginRequiredMixin, TemplateView,
):
    """View de calendário.

    Através desta view que os usuários poderão ver
    as etapas de um cronograma.

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;

    Perfil:
        - Professor da disciplina;
    """
    template_name = 'timetables/calendar.html'
    model = Stage

    def get_context_data(self, **kwargs):
        """Gera o contexto do template."""
        context = super().get_context_data(**kwargs)

        context['allow_create'] = UserGroup(self.request.user).is_teacher() if self.request.user is not None else False

        return context


class TimetableDetailView(DetailView):
    """View de detalhes do calendário."""
    template_name = 'timetables/detail.html'
    model = Timetable
