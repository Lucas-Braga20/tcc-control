"""
Utils template tags.
"""
from django import template

register = template.Library()


@register.filter
def is_in_list(pk, pk_list):
    return pk in pk_list
