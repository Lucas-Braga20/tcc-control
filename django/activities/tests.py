"""
Implementação dos Testes do app de activities.

Contém os testes para:
    - ActivityConfigurationTest (Atividades);
"""

from django.test import TestCase

from activities.forms import ActivityConfigurationForm
from activities.serializers import ActivityConfigurationSerializer


class ActivityConfigurationTest(TestCase):
    """Teste de Configuração de atividade."""

    def test_fields(self):
        data = {
            'name': 'Termo de abertura de projeto',
            'fields': {"fields": []},
        }
        form = ActivityConfigurationForm(data=data)
        serializer = ActivityConfigurationSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertEqual(form.errors['fields'], ['Pelo menos um campo deve ser inserido.'])
        self.assertIn('Pelo menos um campo deve ser inserido.', serializer.errors.get('fields'))
