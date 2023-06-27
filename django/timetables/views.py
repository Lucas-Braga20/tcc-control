"""
Views to timetables apps.
"""

from django.views.generic import CreateView, TemplateView
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
class TimetableCreateView(CreateView):
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
