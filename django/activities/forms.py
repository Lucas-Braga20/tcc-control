"""
Forms to activities app.
"""

from django import forms

from activities.models import ActivityConfiguration
from activities.utils import validate_fields_json


class ActivityConfigurationForm(forms.ModelForm):
    """
    Activity Configuration form.
    """
    template_abnt = forms.FileField(required=True)

    class Meta:
        model = ActivityConfiguration
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        input_field_classes = 'form-control form-control-solid'

        if self.fields['template_abnt'].widget.attrs.get('class') != None:
            self.fields['template_abnt'].widget.attrs['class'] += f' {input_field_classes}'
        else:
            self.fields['template_abnt'].widget.attrs['class'] = f' {input_field_classes}'

        if self.errors.get('template_abnt') is not None:
            self.fields['template_abnt'].widget.attrs['class'] += ' is-invalid'

    def clean_fields(self):
        """
        Validate "fields" field.
        """
        fields = self.cleaned_data.get('fields')

        if fields is None:
            raise forms.ValidationError('The "fields" field cannot be null.')

        try:
            validate_fields_json(fields_value=fields)
        except Exception as e:
            raise forms.ValidationError(str(e))

        return fields
