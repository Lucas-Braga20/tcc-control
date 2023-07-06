"""
Views to timetables apps.
"""

from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from timetables.models import Timetable, Stage
from timetables.forms import TimetableForm


class TimetableListView(LoginRequiredMixin, TemplateView):
    """
    Timetable list screen.
    """
    template_name = 'timetables/list.html'


class TimetableCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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


class TimetableUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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


class TimetableStageCalendarView(LoginRequiredMixin, TemplateView):
    """
    Timetable calendar view.
    """
    template_name = 'timetables/calendar.html'
    model = Stage
