"""
Utils to activities module.
"""

import json

from core.defaults import ACTIVITY_TYPES

from docxtpl import DocxTemplate, RichText


def validate_fields_json(fields_value):
    """
    Method to validate field "fields".

    The json field must contain the attribute "fields" as array of objects
    contains the attributes: name, key and type.
    """

    fields = fields_value.get('fields')

    if fields is None:
        raise Exception('O campo fields não pode ser nulo.')

    if len(fields) == 0:
        raise Exception('Pelo menos um campo deve ser inserido.')

    for field in fields:
        name = field.get('name')
        key = field.get('key')
        type_attr = field.get('type')

        if name is None or key is None or type_attr is None:
            raise Exception('Um campo não foi inserido corretamente.')

        if type_attr not in ACTIVITY_TYPES:
            raise Exception('Um dos campos está com o tipo incorreto.')
