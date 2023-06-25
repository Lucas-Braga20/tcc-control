"""
Works views.
"""

from typing import Any, Dict
from django.views.generic import TemplateView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from works.models import FinalWorkVersion
from works.forms import FinalWorkVersionForm


class WorkStageView(TemplateView):
    """
    Work Stage screen.
    """
    template_name = 'final-work-stages/list.html'


@method_decorator(csrf_exempt, name='dispatch')
class WorkStageDevelopmentView(SuccessMessageMixin, UpdateView):
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


@method_decorator(csrf_exempt, name='dispatch')
class WorkStageDetailView(TemplateView):
    """
    Work stage detail screen.
    """
    template_name = 'final-work-stages/detail.html'
