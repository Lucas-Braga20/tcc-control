"""
Works URL.
"""

from django.urls import path

from works.views import (WorkStageView, WorkStageDevelopmentView, WorkStageDetailView, WorkProposalCreateView,
                         WorkProposalListView, WorkListView, create_work_stage_development, ChangeRequestListView,
                         WorkMeetingsView)


app_name = 'works'
urlpatterns = [
    path('', WorkListView.as_view(), name='list'),
    path('<uuid:pk>/stages/', WorkStageView.as_view(), name='stages'),
    path('<uuid:pk>/meetings/', WorkMeetingsView.as_view(), name='meetings'),
    path('stages/<uuid:pk>/detail', WorkStageDetailView.as_view(), name='detail'),
    path('development/create/', create_work_stage_development, name='development-create'),
    path('development/<uuid:pk>/', WorkStageDevelopmentView.as_view(), name='development'),
    path('proposal/create', WorkProposalCreateView.as_view(), name='proposal-create'),
    path('proposal/list', WorkProposalListView.as_view(), name='proposal-list'),
    path('change-request/list/', ChangeRequestListView.as_view(), name='change-request-list'),
]
