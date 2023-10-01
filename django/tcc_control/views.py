"""
General views to TCC Control project.
"""

from django.views.generic import RedirectView, TemplateView


class HomeView(RedirectView):
    permanent = False
    query_string = False
    pattern_name = 'timetables:calendar'


class EmailView(TemplateView):
    template_name = 'emails/index.html'
