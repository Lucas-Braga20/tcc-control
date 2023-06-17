"""
Activities URL configuration for tcc_control project.
"""

from django.urls import path

from activities.views import FormularyTest, ActivityConfigurationListView


app_name = 'activities'
urlpatterns = [
    path('', FormularyTest.as_view(), name='formulary-test'),
    path('list/', ActivityConfigurationListView.as_view(), name='activity-configuration-list')
]
