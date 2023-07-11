"""
Permissions template tags.
"""

from django import template

from core.permissions import UserGroup

register = template.Library()


@register.simple_tag
def user_group(user):
    if user:
        return UserGroup(user)

    return None    
