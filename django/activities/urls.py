"""
Activities URL configuration for tcc_control project.
"""

from django.urls import path

from activities.views import (ActivityConfigurationListView, ActivityConfigurationCreateView,
                              ActivityConfigurationUpdateView)


app_name = 'activities'
urlpatterns = [
    path('list/', ActivityConfigurationListView.as_view(), name='list'),
    path('create/', ActivityConfigurationCreateView.as_view(), name='create'),
    path('update/<uuid:pk>', ActivityConfigurationUpdateView.as_view(), name='update'),
]
