"""
Activities Tests.
"""

from django.test import TestCase

from activities.forms import ActivityConfigurationForm


class ActivityConfiguration(TestCase):
    """
    Activity Configuration test.
    """
    def test_fields(self):
        data = {
            'name': 'Termo de abertura de projeto',
            'fields': '{"fields": []}'
        }
        form = ActivityConfigurationForm(data=data)

        self.assertEqual(form.errors['fields'], ['Pelo menos um campo deve ser inserido.'])
