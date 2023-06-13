"""
Tests for meetings app.
"""

from django.test import TestCase

from meetings.models import Meeting


class MeetingTest(TestCase):
    """
    Meeting test.
    """
    fixtures = [
        'tcc_control/fixtures/users.json',
        'tcc_control/fixtures/activity_configurations.json',
        'tcc_control/fixtures/timetables.json',
        'tcc_control/fixtures/steps.json',
        'tcc_control/fixtures/tccworks.json',
        'tcc_control/fixtures/work_steps.json',
        'tcc_control/fixtures/meetings.json',
        'tcc_control/fixtures/approved_meetings.json'
    ]

    @classmethod
    def setUpTestData(cls):
        cls.meeting = Meeting.objects.get(id='e25166fb-6f27-48d9-86ef-2b6ae4f3d0c4')
        return super().setUpTestData()

    def test_approved_meeting(self):
        self.assertEqual(self.meeting.get_is_approved(), False)
