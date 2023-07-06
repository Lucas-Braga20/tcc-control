"""
Utils template tags.
"""
from django import template

register = template.Library()


@register.filter
def is_in_list(pk, pk_list):
    return pk in pk_list


@register.filter
def initials(value):
    names = value.split()
    if len(names) >= 2:
        return names[0][0] + names[1][0]
    elif len(names) == 1:
        return names[0][0]
    else:
        return ''
