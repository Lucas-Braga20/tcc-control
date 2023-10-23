"""
Implementação das Views do app raiz.

Contém as views para:
    - HomeView;
"""

from django.views.generic import RedirectView


class HomeView(RedirectView):
    """View inicial do projeto.

    Redireciona o usuário para a tela de calendário.
    """

    permanent = False
    query_string = False
    pattern_name = 'timetables:calendar'
