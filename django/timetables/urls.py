"""
Timetable URL configuration for tcc_control project.
"""

from django.urls import path

from timetables.views import TimetableListView


app_name = 'timetables'
urlpatterns = [
    path('list/', TimetableListView.as_view(), name='list'),
]
