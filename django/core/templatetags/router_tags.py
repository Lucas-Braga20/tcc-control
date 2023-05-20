"""
Router template tags.
"""

from django import template

register = template.Library()


@register.simple_tag
def get_primary_menu_is_active(request, module):
    """
    Get Primary Menu is active by request.
    """

    app_name = None

    try:
        resolver_match = request.resolver_match
        if resolver_match:
            app_name = resolver_match.app_name
    except AttributeError:
        return ''

    if app_name == module:
        return 'active'

    return ''


@register.simple_tag
def get_primary_tab_is_active(request, module):
    """
    Get Primary Tab is active by request.
    """

    app_name = None

    try:
        resolver_match = request.resolver_match
        if resolver_match:
            app_name = resolver_match.app_name
    except AttributeError:
        return ''

    if app_name == module:
        return 'active show'

    return ''


@register.simple_tag
def get_link_is_active(request, link):
    """
    Get Link is active by request.
    """

    url_name = None

    try:
        resolver_match = request.resolver_match
        if resolver_match:
            url_name = resolver_match.url_name
    except AttributeError:
        return ''

    if url_name == link:
        return 'active'

    return ''
