"""
Views to timetables apps.
"""

from django.shortcuts import render
from django.views.generic import CreateView

from timetables.models import Timetable
from timetables.forms import TimetableForm


class TimetableCreate(CreateView):
    """
    Timetable view to create object.
    """
    model = Timetable
    form_class = TimetableForm
