"""
Implementação dos Testes do app de activities.

Contém os testes para:
    - ActivityConfigurationTest (Atividades);
"""

from django.test import TestCase

from activities.forms import ActivityConfigurationForm


class ActivityConfigurationTest(TestCase):
    """Teste de Configuração de atividade."""

    def test_fields(self):
        data = {
            'name': 'Termo de abertura de projeto',
            'fields': '{"fields": []}',
        }
        form = ActivityConfigurationForm(data=data)

        self.assertEqual(form.errors['fields'], ['At least one field must be entered.'])
