"""
Tests for works app.
"""

from django.test import TestCase

from works.forms import WorkStepVersionForm
from works.models import WorkStep


class WorkStepVersionTest(TestCase):
    """
    Work Step Version test.
    """
    fixtures = [
        'tcc_control/fixtures/users.json',
        'tcc_control/fixtures/activity_configurations.json',
        'tcc_control/fixtures/timetables.json',
        'tcc_control/fixtures/steps.json',
        'tcc_control/fixtures/tccworks.json',
        'tcc_control/fixtures/work_steps.json',
    ]

    @classmethod
    def setUpTestData(cls):
        cls.work_step = WorkStep.objects.get(id='53b389cf-de59-4564-98a7-94e3db4ab041')
        return super().setUpTestData()

    def test_contents(self):
        data = {
            'content': '{"fields": [{"key": "title"}]}',
            'work_step': self.work_step
        }
        form = WorkStepVersionForm(data=data)

        self.assertEqual(form.errors['content'], ['Um campo não foi inserido corretamente.'])

