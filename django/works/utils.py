"""
Utils to works app.
"""


def validate_stage_content_json(content):
    """
    Method to validate field content.

    The json field must contain the attribute "fields" as array of objects
    contains the attributes: key and value.
    """

    fields = content.get('fields')

    if fields is None:
        raise Exception('The "fields" field cannot be null.')

    for field in fields:
        key = field.get('key')
        value = field.get('value')

        if key is None or value is None:
            raise Exception('A field was not entered correctly.')
