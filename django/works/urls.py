"""
Works URL.
"""

from django.urls import path

from works.views import WorkStageView, WorkStageDevelopmentView


app_name = 'works'
urlpatterns = [
    path('stages/', WorkStageView.as_view(), name='stages'),
    path('development/<uuid:pk>', WorkStageDevelopmentView.as_view(), name='development'),
]
