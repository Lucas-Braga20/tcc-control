"""
Implementação das Views do app raiz.

Contém as views para:
    - HomeView;
"""

from django.views.generic import RedirectView, TemplateView


class HomeView(RedirectView):
    """View inicial do projeto.

    Redireciona o usuário para a tela de calendário.
    """

    permanent = False
    query_string = False
    pattern_name = 'timetables:calendar'


class AboutView(TemplateView):
    """View de about do projeto."""

    template_name = 'about/index.html'
