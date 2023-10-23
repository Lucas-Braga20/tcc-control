"""
Configurações de Urls do app de timetables.

Contém as urls para:
    - Listagem de cronogramas;
    - Criação de cronograma;
    - Atualização de cronograma;
    - Calendário de cronograma;
    - Detalhes de cronograma;
"""

from django.urls import path

from timetables.views import (
    TimetableListView, TimetableCreateView, TimetableUpdateView, TimetableStageCalendarView, TimetableDetailView
)


app_name = 'timetables'
urlpatterns = [
    path('list/', TimetableListView.as_view(), name='list'),
    path('create/', TimetableCreateView.as_view(), name='create'),
    path('update/<uuid:pk>', TimetableUpdateView.as_view(), name='update'),
    path('calendar/', TimetableStageCalendarView.as_view(), name='calendar'),
    path('detail/<uuid:pk>', TimetableDetailView.as_view(), name='detail'),
]
