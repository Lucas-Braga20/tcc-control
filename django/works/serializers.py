"""
Works serializers.
"""

from rest_framework import serializers

from works.models import TCCWork


class TCCWorkSerializer(serializers.ModelSerializer):
    """
    TCCWork Serializer.
    """

    class Meta:
        model = TCCWork
        fields = '__all__'
