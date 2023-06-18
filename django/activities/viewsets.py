"""
Activities Viewsets.
"""

from rest_framework import mixins, viewsets

from activities.models import ActivityConfiguration
from activities.serializers import ActivityConfigurationSerializer

from django_filters.rest_framework import DjangoFilterBackend


class ActivityConfigurationViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Activity Configuration ViewSet.
    """
    queryset = ActivityConfiguration.objects.all()
    serializer_class = ActivityConfigurationSerializer
    model = ActivityConfiguration
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['archived']
