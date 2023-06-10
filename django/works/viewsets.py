"""
TCCWork viewsets.
"""

from rest_framework import viewsets

from works.models import TCCWork, WorkStep, WorkStepVersion
from works.serializers import TCCWorkSerializer, WorkStepSerializer, WorkStepVersionSerializer


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


class WorkStepVersionViewSet(viewsets.ModelViewSet):
    """
    WorkStepVersion viewset provides all http request methods.
    """
    queryset = WorkStepVersion.objects.all()
    serializer_class = WorkStepVersionSerializer
    model = WorkStepVersion
