"""
Works URL.
"""

from django.urls import path

from works.views import WorkStageView


app_name = 'works'
urlpatterns = [
    path('stages/', WorkStageView.as_view(), name='stages'),
]
