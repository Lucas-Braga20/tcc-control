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


@register.simple_tag
def inline_if(value, true_statement, false_statement):
    if value:
        return true_statement
    else:
        return false_statement


@register.simple_tag(takes_context=True)
def assign_if(context, name, expression):
    try:
        result = bool(eval(expression, {}, context))
    except (SyntaxError, NameError):
        result = False
    context[name] = result
    return ''
