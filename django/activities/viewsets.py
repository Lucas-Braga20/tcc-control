"""
Activities Viewsets.
"""

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from activities.models import ActivityConfiguration
from activities.serializers import ActivityConfigurationSerializer

from django_filters.rest_framework import DjangoFilterBackend


class ActivityConfigurationViewSet(mixins.RetrieveModelMixin,
                                   mixins.ListModelMixin,
                                   mixins.UpdateModelMixin,
                                   viewsets.GenericViewSet):
    """
    Activity Configuration ViewSet.
    """
    queryset = ActivityConfiguration.objects.all()
    serializer_class = ActivityConfigurationSerializer
    model = ActivityConfiguration
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['archived']
    permission_classes = []
    authentication_classes = []

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.archived is True:
            if 'archived' in request.data and request.data['archived'] is False:
                instance.archived = False
                instance.save()
                serializer = self.get_serializer(instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data={'detail': 'You can only change an activity setting if it is not archived'},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().update(request, *args, **kwargs)
