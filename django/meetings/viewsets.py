"""
Meeting viewsets.
"""

from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from meetings.models import Meeting
from meetings.serializers import MeetingSerializer


class MeetingViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    """
    Meeting viewset.
    """
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    model = Meeting
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        no_page = self.request.query_params.get('no_page')
        if no_page:
            self.pagination_class = None

        return queryset
