"""
Tests for comments app.
"""

from django.test import TestCase

from works.models import FinalWorkStage
from users.models import User
from comments.forms import CommentForm


class CommentTest(TestCase):
    """
    Comment test.
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
        cls.user = User.objects.get(id='7f7e4d1c-e707-4059-9d1a-27044afb6725')
        return super().setUpTestData()

    def test_author(self):
        data = {
            'description': 'Teste',
            'work_stage': self.final_work_stage,
            'author': self.user
        }
        form = CommentForm(data=data)

        self.assertEqual(form.errors['author'], ['The comment can only be made by a TCC member.'])
