"""
Works views.
"""

from typing import Any, Dict
from django.views.generic import TemplateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from works.models import FinalWorkVersion
from works.forms import FinalWorkVersionForm


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
