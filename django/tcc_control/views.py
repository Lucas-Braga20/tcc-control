"""
General views to TCC Control project.
"""

from django.views.generic import RedirectView


class HomeView(RedirectView):
    permanent = False
    query_string = False
    pattern_name = 'timetables:calendar'
