"""
Tests for works app.
"""

import datetime

from django.test import TestCase

from works.forms import FinalWorkVersionForm, FinalWorkStageForm
from works.models import FinalWorkStage, ChangeRequest, FinalWorkVersion

from core.defaults import WORK_STAGE_COMPLETED, WORK_STAGE_PRESENTED


class FinalWorkStageTest(TestCase):
    """
    Final work stage test.
    """
    fixtures = [
        'tcc_control/fixtures/users.json',
        'tcc_control/fixtures/activity_configurations.json',
        'tcc_control/fixtures/timetables.json',
        'tcc_control/fixtures/stages.json',
        'tcc_control/fixtures/final_works.json',
        'tcc_control/fixtures/final_work_stages.json',
    ]

    @classmethod
    def setUpTestData(cls):
        cls.final_work_stage = FinalWorkStage.objects.get(id='53b389cf-de59-4564-98a7-94e3db4ab041')
        return super().setUpTestData()

    def test_finish_stage(self):
        """
        Integration test used to verify that it will only
        be possible to mark a stage as completed when there
        is at least one development.
        """
        data = {
            'status': WORK_STAGE_COMPLETED,
        }
        form = FinalWorkStageForm(data=data, instance=self.final_work_stage)

        self.assertEqual(form.errors['status'],
                         ['It is only possible to complete the activity if there is a development.'])

    def test_presented_stage(self):
        """
        Integration test used to verify that it will only
        be possible to mark an activity as "presented" when
        today's date is equal to or later than the presentation date.
        """
        data = {
            'status': WORK_STAGE_PRESENTED,
            'presented': True,
        }
        form = FinalWorkStageForm(data=data, instance=self.final_work_stage)

        presentation_date = self.final_work_stage.stage.presentation_date
        today = datetime.date.today()

        if today >= presentation_date:
            self.assertEqual(form.errors.get('status'), None)
        else:
            self.assertEqual(form.errors.get('status'),
                            ['It is only possible to mark a stage as "presented" when today\'s date is the ' \
                             'presentation date or later'])


class FinalWorkVersionTest(TestCase):
    """
    Final work version test.
    """
    fixtures = [
        'tcc_control/fixtures/users.json',
        'tcc_control/fixtures/activity_configurations.json',
        'tcc_control/fixtures/timetables.json',
        'tcc_control/fixtures/stages.json',
        'tcc_control/fixtures/final_works.json',
        'tcc_control/fixtures/final_work_stages.json',
    ]

    @classmethod
    def setUpTestData(cls):
        cls.final_work_stage = FinalWorkStage.objects.get(id='53b389cf-de59-4564-98a7-94e3db4ab041')
        return super().setUpTestData()

    def test_contents(self):
        data = {
            'content': '{"fields": [{"key": "title"}]}',
            'work_stage': self.final_work_stage
        }
        form = FinalWorkVersionForm(data=data)

        self.assertEqual(form.errors['content'], ['A field was not entered correctly.'])

    def test_contents_keys(self):
        """
        Integration test to verify the fields of the activity.
        """
        data = {
            'content': '{"fields": [{"key": "teste", "value": "teste"}]}',
            'work_stage': self.final_work_stage
        }
        form = FinalWorkVersionForm(data=data)

        self.assertEqual(form.errors['content'], ['The content of the activity has invalid fields.'])


class ChangeRequestTest(TestCase):
    """
    Change request test.
    """
    fixtures = [
        'tcc_control/fixtures/users.json',
        'tcc_control/fixtures/activity_configurations.json',
        'tcc_control/fixtures/timetables.json',
        'tcc_control/fixtures/stages.json',
        'tcc_control/fixtures/final_works.json',
        'tcc_control/fixtures/final_work_stages.json',
        'tcc_control/fixtures/change_requests.json',
    ]

    @classmethod
    def setUpTestData(cls):
        cls.change_request = ChangeRequest.objects.get(id='579376e1-2de0-4e70-86fc-f9f6fd3a6a86')
        return super().setUpTestData()

    def test_approve_request(self):
        """
        Integration test to validate the approval of a change request.
        """
        self.change_request.approve_request()
        self.assertEqual(FinalWorkVersion.objects.all().count(), 1)
