"""
Activities URL configuration for tcc_control project.
"""

from django.urls import path

from activities.views import FormularyTest


app_name = 'activities'
urlpatterns = [
    path('', FormularyTest.as_view(), name='formulary-test'),
]
