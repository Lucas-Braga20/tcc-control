"""Utilitários do app de activities."""

from core.defaults import ACTIVITY_TYPES, NOT_COMPLETED_STATUS

from works.models import FinalWorkStage


def validate_fields_json(fields_value):
    """Validação do campo "fields" da atividade.

    O campo JSON deve conter o atributo "fields" como um array de objetos,
    cada objeto contendo: name, key e type.
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


def check_worked_activity(activity):
    """Checa atividades com trabalhos adiantados.

    Função para verificar se uma atividade possui um etapa de
    trabalho com conteúdo adiantado.
    """
    work_stages = FinalWorkStage.objects.filter(stage__activity_configuration=activity.id,
                                                status__in=NOT_COMPLETED_STATUS)

    has_advanced_activities = False

    for work_stage in work_stages:
        last_version = work_stage.get_last_version()
        content = None

        try:
            if last_version:
                content = last_version.content['fields']
        except Exception:
            content = None

        if content:
            for field in content:
                if field['value'] != '' and field['value'] != None:
                    has_advanced_activities = True

    return has_advanced_activities


def update_worked_activity(activity):
    """Atualiza trabalhos com a atividade relacionada."""
    work_stages = FinalWorkStage.objects.filter(
        stage__activity_configuration=activity.id,
        status__in=NOT_COMPLETED_STATUS,
    )

    for work_stage in work_stages:
        last_version = work_stage.get_last_version()

        if last_version:
            activity_fields = activity.fields
            content = []

            for fields in activity_fields['fields']:
                content.append({
                    'key': fields['key'],
                    'value': '',
                })

            last_version.content = {
                'fields': content
            }
            last_version.save()
