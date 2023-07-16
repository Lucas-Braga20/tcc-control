"""
Notification serializers.
"""

from rest_framework import serializers

from notifications.models import Notification, Receiver


class NotificationSerializer(serializers.ModelSerializer):
    """
    Notification Serializer.
    """
    created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'description', 'author', 'receiver', 'created_at']

    def get_created_at(self, obj):
        return obj.get_created_at()
