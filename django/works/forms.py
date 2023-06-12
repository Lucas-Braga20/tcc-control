"""
Forms to works app.
"""

from django import forms

from works.models import WorkStepVersion
from works.utils import validate_step_content_json


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
