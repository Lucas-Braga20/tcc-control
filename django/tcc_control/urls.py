"""Configuração de rotas do projeto TCC Control."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler400, handler404, handler403, handler500

from tcc_control import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('tcc_control.routers')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    path('activities/', include('activities.urls', namespace='activities')),
    path('works/', include('works.urls', namespace='works')),
    path('timetables/', include('timetables.urls', namespace='timetables')),
    path('about/', views.AboutView.as_view(), name='about'),
]


handler400 = views.Error400View.as_view()
handler403 = views.Error403View.as_view()
handler404 = views.Error404View.as_view()
handler500 = views.Error500View.as_view()


if settings.DEBUG:
    urlpatterns = (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
        urlpatterns
    )
