"""
Forms to timetables app.
"""

from django import forms

from timetables.models import Timetable, Stage


class TimetableForm(forms.ModelForm):
    """
    Timetable form.
    """

    class Meta:
        model = Timetable
        fields = '__all__'

    def clean_participants(self):
        """
        Validate participants field.
        """
        participants = self.cleaned_data.get('participants')

        for participant in participants:
            if participant.groups.all().first().name not in ('Orientando', 'Orientadores'):
                raise forms.ValidationError('Participants must have the profile of mentors or mentees.')

        return participants


    def clean_teacher(self):
        """
        Validate teacher field.
        """
        teacher = self.cleaned_data.get('teacher')

        group = teacher.groups.all().first()

        if group.name != 'Professor da disciplina':
            raise forms.ValidationError('This field must be contains user with teacher role.')

        return teacher


class StageForm(forms.ModelForm):
    """
    Stage form.
    """

    class Meta:
        model = Stage
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        send_date_supervisor = cleaned_data.get('send_date_supervisor')
        send_date = cleaned_data.get('send_date')
        presentation_date = cleaned_data.get('presentation_date')

        if start_date:
            if start_date > send_date_supervisor:
                raise forms.ValidationError(
                    {'start_date': 'The date sent to the supervisor must be after the start date'}
                )

            if start_date > send_date:
                raise forms.ValidationError(
                    {'start_date': 'The date sent to the platform must be after the start date'}
                )

            if presentation_date is not None and start_date > presentation_date:
                raise forms.ValidationError({'start_date': 'The submission date must be after the start date'})

        if send_date_supervisor and send_date:
            if send_date_supervisor > send_date:
                raise forms.ValidationError(
                    {'send_date_supervisor': 'The supervisor submission date should be after the platform submission date.'}
                )
