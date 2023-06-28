"""
Views to timetables apps.
"""

from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages.views import SuccessMessageMixin

from timetables.models import Timetable
from timetables.forms import TimetableForm


class TimetableListView(TemplateView):
    """
    Timetable list screen.
    """
    template_name = 'timetables/list.html'


@method_decorator(csrf_exempt, name='dispatch')
class TimetableCreateView(SuccessMessageMixin, CreateView):
    """
    Timetable view to create object.
    """
    template_name = 'timetables/editor.html'
    model = Timetable
    form_class = TimetableForm
    success_url = reverse_lazy('timetables:list')
    success_message = 'Cronograma criado com sucesso.'
    permission_classes = None
    authentication_classes = None


@method_decorator(csrf_exempt, name='dispatch')
class TimetableUpdateView(SuccessMessageMixin, UpdateView):
    """
    Timetable view to update object.
    """
    template_name = 'timetables/editor.html'
    model = Timetable
    form_class = TimetableForm
    success_url = reverse_lazy('timetables:list')
    success_message = 'Cronograma atualizado com sucesso.'
    permission_classes = None
    authentication_classes = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        object = self.get_object()

        context['mentees'] = object.participants.filter(groups__name='Orientando').values_list('id', flat=True)
        context['supervisors'] = object.participants.filter(groups__name='Orientador').values_list('id', flat=True)

        return context
