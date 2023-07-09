"""
Forms to works app.
"""

import datetime
from typing import Any, Dict

from django import forms

from works.models import FinalWorkStage, FinalWorkVersion, FinalWork
from works.utils import validate_stage_content_json

from users.models import User

from core.defaults import WORK_STAGE_COMPLETED, WORK_STAGE_COMPLETED_LATE, WORK_STAGE_PRESENTED



class FinalWorkForm(forms.ModelForm):
    """
    Final work form.
    """
    mentees = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_active=True, groups__name='Orientando'))
    supervisor = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True, groups__name='Orientador'))

    class Meta:
        model = FinalWork
        fields = ['description', 'supervisor', 'mentees']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

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

        works = FinalWork.objects.filter(approved=True, mentees__in=mentees.values_list('id'))
        if works.exists():
            raise forms.ValidationError(
                'There is already a TCC proposal pending. Cancel the active proposal and create a new one.'
            )

        return cleaned_data


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

        if self.instance is not None and status == WORK_STAGE_PRESENTED:
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
