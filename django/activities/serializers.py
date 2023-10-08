"""
Activities serializers.
"""

import os

from rest_framework import serializers

from activities.models import ActivityConfiguration
from activities.utils import validate_fields_json


class ActivityConfigurationSerializer(serializers.ModelSerializer):
    """
    Activity Configuration Serializer.
    """
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
        fields = obj.fields.get('fields')

        if fields is not None:
            return ', '.join([field['name'] for field in fields])

        return None

    def validate_fields(self, value):
        if value is None:
            raise serializers.ValidationError('The "fields" field cannot be null.')

        try:
            validate_fields_json(fields_value=value)
        except Exception as e:
            raise serializers.ValidationError(str(e))

        return value
