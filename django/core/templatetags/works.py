from django import template


register = template.Library()


@register.simple_tag
def calculate_height_percentage(value):
    """
    Calcula min-height e height em porcentagem com base no valor fornecido.
    O valor deve estar entre 0 e 1.
    """
    if not 0 <= value <= 1:
        raise ValueError('O valor deve estar entre 0 e 1.')

    min_height = value * 100
    height = value * 100

    return f"style='min-height: {min_height}%; height: {height}%;'"


@register.simple_tag
def calculate_percentage(value):
    """
    Multiplica o valor por 100 e retorna o resultado formatado com duas casas decimais.
    O valor deve estar entre 0 e 1.
    """
    if not 0 <= value <= 1:
        raise ValueError('O valor deve estar entre 0 e 1.')

    result = value * 100

    return '{:.2f}'.format(result)


@register.simple_tag
def get_score_color(value):
    """
    Recupera a cor do texto baseado no score do TCC.
    O valor deve estar entre -1 e 1.
    """

    if value == -1:
        return 'text-danger'

    if value == 1:
        return 'text-success'

    return 'text-gray-700'


@register.simple_tag
def get_score_background(value):
    """
    Recupera a cor do background baseado no score do TCC.
    O valor deve estar entre -1 e 1.
    """

    if value == -1:
        return 'bg-danger'

    if value == 1:
        return 'bg-success'

    return 'bg-gray-700'


@register.simple_tag
def get_score_label(value):
    """
    Recupera a label baseado no score do TCC.
    O valor deve estar entre -1 e 1.
    """

    if value == -1:
        return 'Péssimo'

    if value == 1:
        return 'Ótimo'

    return 'Regular'
