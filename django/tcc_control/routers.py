"""
Django rest router.
"""

from rest_framework.routers import DefaultRouter

from activities.viewsets import ActivityConfigurationViewSet
from timetables.viewsets import TimetableViewSet


router = DefaultRouter()
router.register('activities', ActivityConfigurationViewSet)
router.register('timetables', TimetableViewSet)
