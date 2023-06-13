"""
Forms to works app.
"""

import datetime

from django import forms

from works.models import WorkStep, WorkStepVersion
from works.utils import validate_step_content_json

from core.defaults import WORK_STEP_COMPLETED, WORK_STEP_COMPLETED_LATE, WORK_STEP_PRESENTED


class WorkStepForm(forms.ModelForm):
    """
    Work step form.
    """

    class Meta:
        model = WorkStep
        fields = '__all__'

    def clean_status(self):
        """
        Validate status field.
        """
        status = self.cleaned_data.get('status')

        if self.instance is not None and status in (WORK_STEP_COMPLETED, WORK_STEP_COMPLETED_LATE):
            versions = self.instance.step_version.all()

            if not versions.exists():
                raise forms.ValidationError('It is only possible to complete the activity if there is a development.')

        if self.instance is not None and status == WORK_STEP_PRESENTED:
            step = self.instance.step

            today = datetime.date.today()

            if step.presentation_date is None:
                raise forms.ValidationError('It is only possible to mark an activity as "presented" when the ' \
                                            'stage has a presentation.')

            if today < step.presentation_date:
                raise forms.ValidationError('It is only possible to mark a stage as "presented" when today\'s date ' \
                                            'is the presentation date or later')

        return status


class WorkStepVersionForm(forms.ModelForm):
    """
    Work step version form.
    """

    class Meta:
        model = WorkStepVersion
        fields = '__all__'

    def clean_content(self):
        """
        Validate content field.
        """
        content = self.cleaned_data.get('content')

        if content is None:
            raise forms.ValidationError('O campo content não pode ser nulo.')

        try:
            validate_step_content_json(content=content)
        except Exception as e:
            raise forms.ValidationError(str(e))

        return content
