"""
Forms to works app.
"""

import datetime

from django import forms

from works.models import FinalWorkStage, FinalWorkVersion
from works.utils import validate_stage_content_json

from core.defaults import WORK_STAGE_COMPLETED, WORK_STAGE_COMPLETED_LATE, WORK_STAGE_PRESENTED


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
