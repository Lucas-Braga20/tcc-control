"""
Views to timetables apps.
"""

from django.views.generic import CreateView, TemplateView

from timetables.models import Timetable
from timetables.forms import TimetableForm


class TimetableListView(TemplateView):
    """
    Timetable list screen.
    """
    template_name = 'timetables/list.html'


class TimetableCreate(CreateView):
    """
    Timetable view to create object.
    """
    model = Timetable
    form_class = TimetableForm
