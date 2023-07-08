"""
Works views.
"""

from typing import Any, Dict
from django.views.generic import TemplateView, UpdateView, CreateView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from works.models import FinalWorkVersion, FinalWork
from works.forms import FinalWorkVersionForm, FinalWorkForm


class WorkStageView(LoginRequiredMixin, TemplateView):
    """
    Work Stage screen.
    """
    template_name = 'final-work-stages/list.html'


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

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        detail_object = context['object']
        context['fields'] = detail_object.work_stage.stage.activity_configuration.fields

        return context


class WorkStageDetailView(LoginRequiredMixin, TemplateView):
    """
    Work stage detail screen.
    """
    template_name = 'final-work-stages/detail.html'


class WorkProposalCreateView(LoginRequiredMixin, CreateView, View):
    """
    Work proposal create screen.
    """
    template_name = 'final-work-proposal/editor.html'
    model = FinalWork
    form_class = FinalWorkForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
