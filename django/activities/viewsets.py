"""
Activities Viewsets.
"""

from rest_framework import viewsets

from activities.models import ActivityConfiguration
from activities.serializers import ActivityConfigurationSerializer


class ActivityConfigurationViewSet(viewsets.ModelViewSet):
    queryset = ActivityConfiguration.objects.all()
    serializer_class = ActivityConfigurationSerializer
    model = ActivityConfiguration
