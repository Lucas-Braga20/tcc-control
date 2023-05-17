"""
URL configuration for tcc_control project.
"""

from django.contrib import admin
from django.urls import path

from tcc_control import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
]
