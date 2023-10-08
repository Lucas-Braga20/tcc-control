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
    """Formulário de calendário."""
    document_template = forms.FileField(required=True)
    mentee_field = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='Orientando'),
        widget=CustomSelectMultiple(), required=True,
    )
    supervisor_field = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='Orientador'),
        widget=CustomSelectMultiple(), required=True,
    )
    teacher = forms.ModelChoiceField(
        label='Teacher',
        queryset=User.objects.filter(groups__name='Professor da disciplina'),
        widget=forms.Select(attrs={'readonly': 'readonly', 'class': 'd-none'}),
    )

    class Meta:
        model = Timetable
        fields = [
            'mentee_field', 'supervisor_field', 'description', 'teacher',
            'document_template',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Choice
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

    def clean_document_template(self):
        """Valida o campo template.

        Esse campo não pode ter formato diferente de docx e doc.
        Seu tamanho máximo não pode exceder 10 MB.
        """
        document_template = self.cleaned_data.get('document_template')

        if document_template:
            allowed_extensions = ['.docx', '.doc']
            if not any(document_template.name.lower().endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError("Somente arquivos .docx e .doc são permitidos.")

            max_size = 10 * 1024 * 1024  # 10 MB
            if document_template.size > max_size:
                raise forms.ValidationError("O tamanho máximo do arquivo é de 10 MB.")

        return document_template

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()

        mentees = self.cleaned_data.get('mentee_field')
        supervisors = self.cleaned_data.get('supervisor_field')

        participants = instance.participants.values_list('id', flat=True)

        if mentees:
            # Adiciona os novos orientandos.
            for mentee in mentees:
                if mentee.id not in participants.values_list('id', flat=True):
                    instance.participants.add(mentee)

            # Remove todos os orientandos.
            for participant in participants.filter(groups__name='Orientando'):
                if participant not in mentees.values_list('id', flat=True):
                    instance.participants.remove(participant)

        if supervisors:
            # Adiciona os novos orientadores.
            for supervisor in supervisors:
                if supervisor.id not in participants.values_list('id', flat=True):
                    instance.participants.add(supervisor)

            # Remove todos os orientadores.
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
