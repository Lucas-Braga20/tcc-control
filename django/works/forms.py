"""
Forms to works app.
"""

import datetime
from typing import Any

from django import forms

from works.models import FinalWorkStage, FinalWorkVersion, FinalWork
from works.utils import validate_stage_content_json

from users.models import User

from core.defaults import (
    WORK_STAGE_COMPLETED, WORK_STAGE_COMPLETED_LATE, WORK_STAGE_PRESENTED, WORK_STAGE_ADJUSTED, WORK_STAGE_ASSIGNED,
    WORK_STAGE_PRESENTED_LATE,
)


class FinalWorkForm(forms.ModelForm):
    """Formulário de TCC."""
    mentees = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_active=True, groups__name='Orientando'))
    supervisor = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True, groups__name='Orientador'))
    title = forms.CharField(
        widget=forms.TextInput(),
        max_length=128,
        required=True,
        label='Título do seu TCC',
    )

    class Meta:
        model = FinalWork
        fields = ['description', 'supervisor', 'mentees', 'title']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        self.user = user

        super().__init__(*args, **kwargs)

        self.fields['description'].widget.attrs.update({
            'maxlength': 255,
            'minlength': 3,
        })

        if user:
            self.fields['mentees'].initial = user

        self.fields['mentees'].widget.attrs.update({
            'data-control': 'select2',
            'data-close-on-select': 'false',
            'data-placeholder': 'Selecione os orientandos',
            'data-allow-clear': 'true',
            'multiple': 'true',
        })

        self.fields['supervisor'].widget.attrs.update({
            'data-control': 'select2',
            'data-placeholder': 'Selecione o orientador',
        })

    def clean(self):
        cleaned_data = super().clean()
        mentees = cleaned_data.get('mentees')

        works = FinalWork.objects.filter(
            mentees__in=mentees.values_list('id'),
        ).exclude(archived=True).exclude(approved=False)

        if works.exists():
            raise forms.ValidationError(
                'Já existe uma proposta de TCC pendente. Cancele a proposta ativa e crie uma nova.'
            )

        return cleaned_data

    def save(self, commit: bool = ...) -> Any:
        if self.user is None:
            raise forms.ValidationError(
                'É necessário estar autenticado para criar uma proposta.'
            )

        timetable = self.user.get_current_timetable()
        if timetable is None:
            self.add_error(
                None,
                forms.ValidationError(
                    'É necessário estar vinculado a um cronograma com etapas para criar uma proposta.',
                ),
            )
            raise Exception('Proposal form error.')

        instance = super().save(commit=False)
        instance.timetable = timetable

        if commit:
            self.instance.save()
            self._save_m2m()
        else:
            self.save_m2m = self._save_m2m

        return instance


class FinalWorkStageForm(forms.ModelForm):
    """
    Final work stage form.
    """

    class Meta:
        model = FinalWorkStage
        fields = '__all__'

    def clean(self):
        """
        Validate status field.
        """
        status = self.cleaned_data.get('status')

        if self.instance is not None and status in (WORK_STAGE_COMPLETED, WORK_STAGE_COMPLETED_LATE):
            versions = self.instance.work_stage_version.all()

            if not versions.exists():
                raise forms.ValidationError(
                    {'status': 'It is only possible to complete the activity if there is a development.'}
                )

        if self.instance is not None and (status == WORK_STAGE_PRESENTED or status == WORK_STAGE_PRESENTED_LATE):
            timetable_stage = self.instance.stage

            today = datetime.date.today()

            if timetable_stage.presentation_date is None:
                raise forms.ValidationError(
                    {'status': 'It is only possible to mark an activity as "presented" when the stage has a presentation.'}
                )

            if today < timetable_stage.presentation_date:
                raise forms.ValidationError(
                    {'status': 'It is only possible to mark a stage as "presented" when today\'s date is the presentation date or later'}
                )


class FinalWorkVersionForm(forms.ModelForm):
    """
    Final work version form.
    """

    class Meta:
        model = FinalWorkVersion
        fields = ['content']

    def clean_content(self):
        """
        Validate content field.
        """
        content = self.cleaned_data.get('content')

        if content is None:
            raise forms.ValidationError('The content field cannot be null.')

        try:
            validate_stage_content_json(content=content)
        except Exception as e:
            raise forms.ValidationError(str(e))

        return content

    def clean(self):
        content = self.cleaned_data.get('content')

        work_stage = self.instance.work_stage

        if content is not None:
            activity_configuration = work_stage.stage.activity_configuration

            activity_fields = activity_configuration.fields.get('fields')
            keys = [activity_field.get('key') for activity_field in activity_fields]

            for content_field in content.get('fields'):
                if content_field['key'] not in keys:
                    raise forms.ValidationError({'content': 'The content of the activity has invalid fields.'})

    def save(self, commit=True):
        instance = super().save(commit=False)

        if instance.work_stage.status == WORK_STAGE_ADJUSTED:
            instance.work_stage.status = WORK_STAGE_ASSIGNED

        if commit:
            instance.work_stage.save()

        instance.save()

        return instance


class FinalWorkCreateVersionForm(forms.ModelForm):
    """
    Final work create version form.
    """

    class Meta:
        model = FinalWorkVersion
        fields = ['work_stage']

    def save(self, commit):
        version = super().save(commit)

        activity_fields = version.work_stage.stage.activity_configuration.fields
        content = []

        for fields in activity_fields['fields']:
            content.append({
                'key': fields['key'],
                'value': '',
            })

        version.content = {
            'fields': content
        }
        version.save()

        return version
