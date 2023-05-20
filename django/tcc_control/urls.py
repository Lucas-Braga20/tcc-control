"""
URL configuration for tcc_control project.
"""

from django.contrib import admin
from django.urls import path, include

from tcc_control import views
from tcc_control.routers import router


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('formulary-test/', include('activities.urls', namespace='formulary-test')),
]
