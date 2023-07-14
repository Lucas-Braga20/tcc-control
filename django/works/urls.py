"""
Works URL.
"""

from django.urls import path

from works.views import (WorkStageView, WorkStageDevelopmentView, WorkStageDetailView, WorkProposalCreateView,
                         WorkProposalListView, WorkListView)


app_name = 'works'
urlpatterns = [
    path('', WorkListView.as_view(), name='list'),
    path('<uuid:pk>/stages/', WorkStageView.as_view(), name='stages'),
    path('stages/detail', WorkStageDetailView.as_view(), name='detail'),
    path('development/<uuid:pk>', WorkStageDevelopmentView.as_view(), name='development'),
    path('proposal/create', WorkProposalCreateView.as_view(), name='proposal-create'),
    path('proposal/list', WorkProposalListView.as_view(), name='proposal-list'),
]
