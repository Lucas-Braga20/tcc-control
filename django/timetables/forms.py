"""
Forms to timetables app.
"""

from django import forms

from timetables.models import Timetable


class TimetableForm(forms.ModelForm):
    """
    Timetable form.
    """

    class Meta:
        model = Timetable
        fields = '__all__'
