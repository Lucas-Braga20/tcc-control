"""
Implementação dos Formulários do app de timetables.

Contém os formulários para:
    - TimetableForm (Cronograma);
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
            'mentee_field', 'supervisor_field', 'description', 'teacher', 'document_template',
        ]

    def __init__(self, *args, **kwargs):
        self.is_creation = kwargs.pop('is_creation', False)

        super().__init__(*args, **kwargs)

        # Choice
        self.fields['mentee_field'].choices = [
            (user.pk, user.get_full_name()) for user in User.objects.filter(groups__name='Orientando')
        ]
        self.fields['supervisor_field'].choices = [
            (user.pk, user.get_full_name()) for user in User.objects.filter(groups__name='Orientador')
        ]

    def clean_participants(self):
        """Valida campo de participantes.

        Não é possível adicionar um participante que já esteja
        em outro cronograma.
        """
        participants = self.cleaned_data.get('participants')

        for participant in participants:
            if participant.groups.all().first().name not in ('Orientando', 'Orientadores'):
                raise forms.ValidationError('Os participantes devem ter perfil de orientando ou orientador.')

            if (
                participant.groups.all().first().name == 'Orientando' and
                participant.get_current_timetable() is not None
            ):
                raise forms.ValidationError('Já existe participante vinculado a um cronograma.')

        return participants

    def clean_mentee_field(self):
        """Valida campo de orientando.

        Não é possível adicionar um orientando que já esteja
        em outro cronograma.
        """
        mentees = self.cleaned_data.get('mentee_field')

        if self.is_creation is False:
            return mentees

        for mentee in mentees:
            if mentee.groups.all().first().name != 'Orientando':
                raise forms.ValidationError('Os orientandos devem ter perfil de orientando.')

            if mentee.get_current_timetable() is not None:
                raise forms.ValidationError('Já existe orientando vinculado a um cronograma.')

        return mentees

    def clean_supervisor_field(self):
        """Valida campo de orientador.

        Não é possível adicionar um participante que não tenha
        perfil de orientador.
        """
        supervisors = self.cleaned_data.get('supervisor_field')

        if self.is_creation is False:
            return supervisors

        for supervisor in supervisors:
            if supervisor.groups.all().first().name != 'Orientador':
                raise forms.ValidationError('Os orientandores devem ter perfil de orientandor.')

        return supervisors

    def clean_teacher(self):
        """Valida campo de professor.

        Não é possível adicionar um participante que não tenha
        perfil de professor.
        """
        teacher = self.cleaned_data.get('teacher')

        group = teacher.groups.all().first()

        if group.name != 'Professor da disciplina':
            raise forms.ValidationError('Esse campo deve conter um usuário com perfil de professor.')

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
        """Salva a instância do Cronograma.

        Cria o relacionamento entre cronograma e participantes."""
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
    """Formulário de Etapas."""

    class Meta:
        model = Stage
        fields = '__all__'

    def clean(self):
        """Valida todos os campos do formulário.

        A datas de envio ao supervisor, envio a plataforma
        deve ser após a data de início.

        A data de envio a plataforma deve ser antes da data de apresentação.

        A data de envio ao orientador deve ser antes da data de envio."""
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        send_date_supervisor = cleaned_data.get('send_date_supervisor')
        send_date = cleaned_data.get('send_date')
        presentation_date = cleaned_data.get('presentation_date')

        if start_date:
            if start_date > send_date_supervisor:
                raise forms.ValidationError(
                    {'start_date': 'A data de envio ao supervisor deve ser após a data de início'}
                )

            if start_date > send_date:
                raise forms.ValidationError(
                    {'start_date': 'A data de envio a plataforma deve ser após a data de início'}
                )

            if presentation_date is not None and start_date > presentation_date:
                raise forms.ValidationError({
                    'start_date': 'A data de envio a plataforma deve ser após a data de início.',
                })

        if send_date_supervisor and send_date:
            if send_date_supervisor > send_date:
                raise forms.ValidationError(
                    {'send_date_supervisor': 'A data de envio ao orientador deve ser antes da data de envio.'}
                )
