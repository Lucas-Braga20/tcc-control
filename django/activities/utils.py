"""
Utils to activities app.
"""

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
        raise Exception('The "fields" field cannot be null.')

    if len(fields) == 0:
        raise Exception('At least one field must be entered.')

    for field in fields:
        name = field.get('name')
        key = field.get('key')
        type_attr = field.get('type')

        if name is None or key is None or type_attr is None:
            raise Exception('A field was not entered correctly.')

        if type_attr not in ACTIVITY_TYPES:
            raise Exception('Um dos campos está com o tipo incorreto.')
