"""
Works URL.
"""

from django.urls import path

from works.views import (WorkStageView, WorkStageDevelopmentView, WorkStageDetailView, WorkProposalCreateView,
                         WorkProposalListView)


app_name = 'works'
urlpatterns = [
    path('stages/', WorkStageView.as_view(), name='stages'),
    path('stages/detail', WorkStageDetailView.as_view(), name='detail'),
    path('development/<uuid:pk>', WorkStageDevelopmentView.as_view(), name='development'),
    path('proposal/create', WorkProposalCreateView.as_view(), name='proposal-create'),
    path('proposal/list', WorkProposalListView.as_view(), name='proposal-list'),
]
