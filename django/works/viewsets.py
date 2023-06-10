"""
TCCWork viewsets.
"""

from rest_framework import viewsets

from works.models import TCCWork, WorkStep
from works.serializers import TCCWorkSerializer, WorkStepSerializer


class TCCWorkViewSet(viewsets.ModelViewSet):
    """
    TCCWork viewset provides all http request methods.
    """
    queryset = TCCWork.objects.all()
    serializer_class = TCCWorkSerializer
    model = TCCWork


class WorkStepViewSet(viewsets.ModelViewSet):
    """
    WorkStep viewset provides all http request methods.
    """
    queryset = WorkStep.objects.all()
    serializer_class = WorkStepSerializer
    model = WorkStep
