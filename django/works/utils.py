"""
Utils to works app.
"""


def validate_step_content_json(content):
    """
    Method to validate field content.

    The json field must contain the attribute "fields" as array of objects
    contains the attributes: key and value.
    """

    fields = content.get('fields')

    if fields is None:
        raise Exception('O campo fields não pode ser nulo.')

    for field in fields:
        key = field.get('key')
        value = field.get('value')

        if key is None or value is None:
            raise Exception('Um campo não foi inserido corretamente.')
