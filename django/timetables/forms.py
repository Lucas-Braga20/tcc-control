"""
Forms to timetables app.
"""

from django import forms

from timetables.models import Timetable, Stage

from users.models import User


class CustomSelectMultiple(forms.SelectMultiple):
    def render_option(self, selected_choices, option_value, option_label):
        user = User.objects.get(pk=option_value)
        option_label = user.get_full_name()
        return super().render_option(selected_choices, option_value, option_label)


class TimetableForm(forms.ModelForm):
    """
    Timetable form.
    """
    mentee_field = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='Orientando'),
        widget=CustomSelectMultiple(),
        required=True
    )
    supervisor_field = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='Orientador'),
        widget=CustomSelectMultiple(),
        required=True
    )
    teacher = forms.ModelChoiceField(
        label='Teacher',
        queryset=User.objects.filter(username='joao.amancio'),
        initial=User.objects.get(username='joao.amancio'),
        widget=forms.Select(attrs={'readonly': 'readonly', 'class': 'd-none'})
    )

    class Meta:
        model = Timetable
        fields = ['mentee_field', 'supervisor_field', 'description', 'teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['mentee_field'].choices = [
            (user.pk, user.get_full_name()) for user in User.objects.filter(groups__name='Orientando')
        ]
        self.fields['supervisor_field'].choices = [
            (user.pk, user.get_full_name()) for user in User.objects.filter(groups__name='Orientador')
        ]

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

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()

        mentees = self.cleaned_data.get('mentee_field')
        supervisors = self.cleaned_data.get('supervisor_field')

        participants = instance.participants.values_list('id', flat=True)

        if mentees:
            # add mentees
            for mentee in mentees:
                if mentee.id not in participants.values_list('id', flat=True):
                    instance.participants.add(mentee)

            # remove mentees
            for participant in participants.filter(groups__name='Orientando'):
                if participant not in mentees.values_list('id', flat=True):
                    instance.participants.remove(participant)
        if supervisors:
            # add supervisor
            for supervisor in supervisors:
                if supervisor.id not in participants.values_list('id', flat=True):
                    instance.participants.add(supervisor)

            # remove supervisor
            for participant in participants.filter(groups__name='Orientador'):
                if participant not in supervisors.values_list('id', flat=True):
                    instance.participants.remove(participant)

        if commit:
            instance.save()

        return instance


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
