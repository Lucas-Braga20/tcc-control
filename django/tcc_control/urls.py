"""
URL configuration for tcc_control project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from tcc_control import views
from tcc_control.routers import router


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('tcc_control.routers')),
    path('activities/', include('activities.urls', namespace='activities')),
    path('works/', include('works.urls', namespace='works')),
]


if settings.DEBUG:
    urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
