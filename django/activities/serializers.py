"""
Activities serializers.
"""

from rest_framework import serializers

from activities.models import ActivityConfiguration


class ActivityConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityConfiguration
        fields = '__all__'
