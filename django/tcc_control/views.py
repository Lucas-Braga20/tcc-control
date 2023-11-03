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


class Error404View(TemplateView):
    """View de erro 404."""

    template_name = 'errors/404.html'


class Error400View(TemplateView):
    """View de erro 400."""

    template_name = 'errors/400.html'


class Error401View(TemplateView):
    """View de erro 401."""

    template_name = 'errors/401.html'


class Error403View(TemplateView):
    """View de erro 403."""

    template_name = 'errors/403.html'


class Error500View(TemplateView):
    """View de erro 500."""

    template_name = 'errors/500.html'
