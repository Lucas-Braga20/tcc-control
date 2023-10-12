"""
Configurações de Urls do app de activities.

Contém as urls para:
    - Listagem de atividades;
    - Criação de atividades;
    - Atualização de atividades;
"""

from django.urls import path

from activities.views import (
    ActivityConfigurationListView, ActivityConfigurationCreateView, ActivityConfigurationUpdateView,
)


app_name = 'activities'
urlpatterns = [
    path('list/', ActivityConfigurationListView.as_view(), name='list'),
    path('create/', ActivityConfigurationCreateView.as_view(), name='create'),
    path('update/<uuid:pk>', ActivityConfigurationUpdateView.as_view(), name='update'),
]
