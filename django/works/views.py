"""
Works views.
"""

from django.views.generic import TemplateView, UpdateView, CreateView, View, ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.urls import reverse_lazy

from works.models import FinalWorkVersion, FinalWork
from works.forms import FinalWorkVersionForm, FinalWorkForm

from users.models import User

from meetings.models import Meeting

from core.permissions import UserGroup, GenericPermissionMixin


class WorkStageView(LoginRequiredMixin, DetailView, View):
    """
    Work Stage screen.
    """
    template_name = 'final-work-stages/list.html'
    model = FinalWork

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        object = self.get_object()

        context['meetings'] = Meeting.objects.filter(work_stage__final_work=object).exclude(
            meeting_approved__approved=False
        )

        return context


class WorkStageDevelopmentView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Work stage development view.
    """
    template_name = 'final-work-versions/editor.html'
    model = FinalWorkVersion
    form_class = FinalWorkVersionForm
    success_url = reverse_lazy('works:stages')
    success_message = 'Trabalho salvo com sucesso.'
    permission_classes = None
    authentication_classes = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        detail_object = context['object']
        context['fields'] = detail_object.work_stage.stage.activity_configuration.fields

        return context


class WorkStageDetailView(LoginRequiredMixin, TemplateView):
    """
    Work stage detail screen.
    """
    template_name = 'final-work-stages/detail.html'


class WorkProposalCreateView(GenericPermissionMixin, LoginRequiredMixin, CreateView, View):
    """
    Work proposal create screen.
    """
    template_name = 'final-work-proposal/editor.html'
    model = FinalWork
    form_class = FinalWorkForm
    success_url = reverse_lazy('works:proposal-list')
    success_message = 'Proposta de TCC criada com sucesso.'
    required_groups = ['Orientando']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class WorkProposalListView(LoginRequiredMixin, ListView, View):
    """
    Work proposal list screen.
    """
    template_name = 'final-work-proposal/list.html'
    model = FinalWork

    def get_queryset(self):
        queryset = super().get_queryset()

        user_group = UserGroup(self.request.user)

        if user_group.is_mentee():
            queryset = queryset.filter(mentees__in=[self.request.user])

        if user_group.is_supervisor():
            queryset = queryset.filter(supervisor=self.request.user)

        queryset = queryset.exclude(archived=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['supervisor'] = User.objects.filter(groups__name='Orientador')
        context['mentee_group'] = Group.objects.get(name='Orientando')
        context['teacher_group'] = Group.objects.get(name='Professor da disciplina')
        context['allow_create'] = not FinalWork.objects.filter(
            mentees__in=[self.request.user]
        ).exclude(archived=True).exists()

        return context


class WorkListView(GenericPermissionMixin, LoginRequiredMixin, TemplateView):
    """
    Final work list screen.
    """
    template_name = 'final-work/list.html'
    required_groups = ['Orientador', 'Professor da disciplina']
