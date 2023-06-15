"""
Tests for activities app.
"""

from django.test import TestCase

from activities.forms import ActivityConfigurationForm


class ActivityConfigurationTest(TestCase):
    """
    Activity Configuration test.
    """
    def test_fields(self):
        data = {
            'name': 'Termo de abertura de projeto',
            'fields': '{"fields": []}'
        }
        form = ActivityConfigurationForm(data=data)

        self.assertEqual(form.errors['fields'], ['At least one field must be entered.'])
