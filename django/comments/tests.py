"""
Tests for comments app.
"""

from django.test import TestCase

from works.models import WorkStep
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
        'tcc_control/fixtures/steps.json',
        'tcc_control/fixtures/tccworks.json',
        'tcc_control/fixtures/work_steps.json',
    ]

    @classmethod
    def setUpTestData(cls):
        cls.work_step = WorkStep.objects.get(id='53b389cf-de59-4564-98a7-94e3db4ab041')
        cls.user = User.objects.get(id='7f7e4d1c-e707-4059-9d1a-27044afb6725')
        return super().setUpTestData()

    def test_author(self):
        data = {
            'description': 'Teste',
            'work_step': self.work_step,
            'author': self.user
        }
        form = CommentForm(data=data)

        self.assertEqual(form.errors['author'], ['The comment can only be made by a TCC member.'])
