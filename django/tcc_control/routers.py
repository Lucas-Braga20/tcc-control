"""
Django rest router.
"""

from rest_framework.routers import DefaultRouter

from activities.viewsets import ActivityConfigurationViewSet
from timetables.viewsets import TimetableViewSet, StepViewSet
from works.viewsets import TCCWorkViewSet


router = DefaultRouter()
router.register('activities', ActivityConfigurationViewSet)
router.register('timetables', TimetableViewSet)
router.register('steps', StepViewSet)
router.register('tcc-works', TCCWorkViewSet)
