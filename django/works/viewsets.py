"""
TCCWork viewsets.
"""

from rest_framework import viewsets

from works.models import TCCWork
from works.serializers import TCCWorkSerializer


class TCCWorkViewSet(viewsets.ModelViewSet):
    """
    TCCWork viewset provides all http request methods.
    """
    queryset = TCCWork.objects.all()
    serializer_class = TCCWorkSerializer
    model = TCCWork
