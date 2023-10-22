"""
Implementação dos Serializers do app de activities.

Contém os serializers para:
    - ActivityConfigurationSerializer (Atividades);
"""

from rest_framework import serializers

from activities.models import ActivityConfiguration
from activities.utils import validate_fields_json


class ActivityConfigurationSerializer(serializers.ModelSerializer):
    """Serializer de Configuração de atividade."""
    fields_description = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ActivityConfiguration
        fields = ['id', 'name', 'fields', 'fields_description', 'document_insertion', 'archived']
        datatables_always_serialize = ('id', 'name', 'fields', 'fields_description', 'document_insertion', 'archived')
        depth = 2
        extra_kwargs = {
            'fields': {'write_only': True}
        }

    def get_fields_description(self, obj):
        """Retorna o valor descritivo do campo "fields"."""
        fields = obj.fields.get('fields')

        if fields is not None:
            return ', '.join([field['name'] for field in fields])

        return None

    def validate_fields(self, value):
        """Validação do campos "fields"."""
        if value is None:
            raise serializers.ValidationError('O campo "fields" não pode ser nulo.')

        try:
            validate_fields_json(fields_value=value)
        except Exception as e:
            raise serializers.ValidationError(str(e))

        return value
