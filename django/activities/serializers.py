"""
Activities serializers.
"""

from rest_framework import serializers

from activities.models import ActivityConfiguration


class ActivityConfigurationSerializer(serializers.ModelSerializer):
    """
    Activity Configuration Serializer.
    """
    fields_description = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ActivityConfiguration
        fields = ['id', 'name', 'fields', 'fields_description', 'template_abnt', 'archived']
        datatables_always_serialize = ('id', 'name', 'fields', 'fields_description', 'template_abnt', 'archived')
        depth = 2
        extra_kwargs = {
            'fields': {'write_only': True}
        }

    def get_fields_description(self, obj):
        fields = obj.fields.get('fields')

        if fields is not None:
            return ', '.join([field['name'] for field in fields])

        return None
