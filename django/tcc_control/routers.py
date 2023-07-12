"""
Django rest router.
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from activities.viewsets import ActivityConfigurationViewSet
from timetables.viewsets import TimetableViewSet, StageViewSet
from works.viewsets import (
    FinalWorkViewSet, FinalWorkStageViewSet, FinalWorkVersionViewSet, ChangeRequestViewSet, VersionContentImageViewSet
)
from comments.viewsets import CommentViewSet
from users.viewsets import UserViewSet


router = DefaultRouter()
router.register('activities', ActivityConfigurationViewSet, basename='activities')
router.register('timetables', TimetableViewSet)
router.register('stages', StageViewSet)
router.register('users', UserViewSet)
router.register('final-works', FinalWorkViewSet, basename='works')
router.register('final-work-stages', FinalWorkStageViewSet)
router.register('final-work-versions', FinalWorkVersionViewSet)
router.register('version-content-images', VersionContentImageViewSet)
router.register('change-requests', ChangeRequestViewSet)
router.register('comments', CommentViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls))
]
