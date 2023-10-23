"""Testes do app de meetings."""

from django.test import TestCase

from meetings.models import Meeting


class MeetingTest(TestCase):
    """Testes de reuniões."""

    fixtures = [
        'tcc_control/fixtures/courses.json',
        'tcc_control/fixtures/users.json',
        'tcc_control/fixtures/activity_configurations.json',
        'tcc_control/fixtures/timetables.json',
        'tcc_control/fixtures/stages.json',
        'tcc_control/fixtures/final_works.json',
        'tcc_control/fixtures/final_work_stages.json',
        'tcc_control/fixtures/tests/meetings.json'
    ]

    @classmethod
    def setUpTestData(cls):
        cls.meeting = Meeting.objects.get(id='3aac2c77-3934-40a6-9725-e92eb8801eac')
        return super().setUpTestData()

    def test_approved_meeting(self):
        """Testa o estado de aprovação da reunião.

        Uma reunião apenas é considerada aprovada se todas as partes
        aprovarem.
        """
        self.assertEqual(self.meeting.get_is_approved(), False)
