"""
Viewsets to works app.
"""

from rest_framework import viewsets

from works.models import FinalWork, FinalWorkStage, FinalWorkVersion, ChangeRequest
from works.serializers import (
    FinalWorkSerializer, FinalWorkStageSerializer, FinalWorkVersionSerializer, ChangeRequestSerializer
)


class FinalWorkViewSet(viewsets.ModelViewSet):
    """
    Final work viewset.
    """
    queryset = FinalWork.objects.all()
    serializer_class = FinalWorkSerializer
    model = FinalWork


class FinalWorkStageViewSet(viewsets.ModelViewSet):
    """
    Final work stage viewset.
    """
    queryset = FinalWorkStage.objects.all()
    serializer_class = FinalWorkStageSerializer
    model = FinalWorkStage


class FinalWorkVersionViewSet(viewsets.ModelViewSet):
    """
    Final work version viewset.
    """
    queryset = FinalWorkVersion.objects.all()
    serializer_class = FinalWorkVersionSerializer
    model = FinalWorkVersion


class ChangeRequestViewSet(viewsets.ModelViewSet):
    """
    Change request viewset.
    """
    queryset = ChangeRequest.objects.all()
    serializer_class = ChangeRequestSerializer
    model = ChangeRequest
