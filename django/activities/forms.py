"""
Implementação dos Formulários do app de activities.

Contém os formulários para:
    - ActivityConfigurationForm (Atividades);
"""

from django import forms

from activities.models import ActivityConfiguration
from activities.utils import validate_fields_json


class ActivityConfigurationForm(forms.ModelForm):
    """Formulário de Configuração de atividade."""

    class Meta:
        model = ActivityConfiguration
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['document_insertion'].value = True

    def clean_fields(self):
        """Validação do campos "fields"."""
        fields = self.cleaned_data.get('fields')

        if fields is None:
            raise forms.ValidationError('O campo "fields" não pode ser nulo.')

        try:
            validate_fields_json(fields_value=fields)
        except Exception as e:
            raise forms.ValidationError(str(e))

        return fields
