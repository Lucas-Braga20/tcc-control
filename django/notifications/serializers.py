"""
Implementação dos Serializers do app de notifications.

Contém os serializers para:
    - NotificationSerializer (Notificação);
"""

from rest_framework import serializers

from notifications.models import Notification

from users.models import User


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer de Notificação."""
    created_at = serializers.SerializerMethodField(read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(), many=True)

    class Meta:
        model = Notification
        fields = ['id', 'description', 'author', 'receiver', 'created_at']

    def get_created_at(self, obj):
        """Retorna o datetime de criação da notificação."""
        return obj.get_created_at()
