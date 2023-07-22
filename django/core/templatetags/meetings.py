"""
Meetings template tags.
"""

from django import template

register = template.Library()


@register.simple_tag
def review_meeting_required(meeting, user):
    return meeting.review_meeting_required(user)
