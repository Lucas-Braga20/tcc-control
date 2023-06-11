"""
Forms to timetables app.
"""

from django import forms

from timetables.models import Timetable, Step


class TimetableForm(forms.ModelForm):
    """
    Timetable form.
    """

    class Meta:
        model = Timetable
        fields = '__all__'


class StepForm(forms.ModelForm):
    """
    Step form.
    """

    class Meta:
        model = Step
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        send_date_advisor = cleaned_data.get('send_date_advisor')
        send_date = cleaned_data.get('send_date')
        presentation_date = cleaned_data.get('presentation_date')

        if start_date:
            if start_date > send_date_advisor:
                raise forms.ValidationError(
                    {'start_date': 'The date sent to the advisor must be after the start date'}
                )

            if start_date > send_date:
                raise forms.ValidationError(
                    {'start_date': 'The date sent to the platform must be after the start date'}
                )

            if presentation_date is not None and start_date > presentation_date:
                raise forms.ValidationError({'start_date': 'The submission date must be after the start date'})

        if send_date_advisor and send_date:
            if send_date_advisor > send_date:
                raise forms.ValidationError(
                    {'send_date_advisor': 'The advisor submission date should be after the platform submission date.'}
                )
