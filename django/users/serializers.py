"""
Implementação dos Serializers do app de users.

Contém os serializers para:
    - GroupSerializer (Cronograma);
    - UserSerializer (Usuário);
"""

from django.contrib.auth.models import Group

from rest_framework import serializers

from users.models import User


class GroupSerializer(serializers.ModelSerializer):
    """Serializer de Grupo do usuário (Cargo)."""

    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Serializer de Usuário."""
    groups_detail = GroupSerializer(many=True, source='groups', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_active', 'phone',
            'groups', 'groups_detail', 'full_name',
        ]
        read_only_fields = [
            'id', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'phone', 'groups_detail',
            'full_name',
        ]

    def get_full_name(self, obj):
        """Recupera o nome completo do usuário."""
        return obj.get_full_name()
