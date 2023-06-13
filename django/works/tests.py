"""
Tests for works app.
"""

from django.test import TestCase

from works.forms import WorkStepVersionForm, WorkStepForm
from works.models import WorkStep

from core.defaults import WORK_STEP_COMPLETED, WORK_STEP_PRESENTED


class WorkStepTest(TestCase):
    """
    Work Step test.
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

    def test_finish_step(self):
        """
        Integration test used to verify that it will only
        be possible to mark a stage as completed when there
        is at least one development.
        """
        data = {
            'status': WORK_STEP_COMPLETED
        }
        form = WorkStepForm(data=data, instance=self.work_step)

        self.assertEqual(form.errors['status'],
                         ['It is only possible to complete the activity if there is a development.'])

    def test_presented_step(self):
        """
        Integration test used to verify that it will only
        be possible to mark an activity as "presented" when
        today's date is equal to or later than the presentation date.
        """
        data = {
            'status': WORK_STEP_PRESENTED
        }
        form = WorkStepForm(data=data, instance=self.work_step)

        self.assertEqual(form.errors['status'],
                         ['It is only possible to mark a stage as "presented" when today\'s date is the ' \
                          'presentation date or later'])


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

    def test_contents_keys(self):
        """
        Integration test to verify the fields of the activity.
        """
        data = {
            'content': '{"fields": [{"key": "teste", "value": "teste"}]}',
            'work_step': self.work_step
        }
        form = WorkStepVersionForm(data=data)

        self.assertEqual(form.errors['content'], ['The content of the activity has invalid fields.'])

