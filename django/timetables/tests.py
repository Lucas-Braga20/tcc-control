"""
Tests for timetables app.
"""

from django.test import TestCase
from django.contrib.auth.models import Group
from django.forms.fields import Field

from timetables.forms import TimetableForm

from users.models import User


class TimetableTest(TestCase):
    """
    Timetable test.
    """
    fixtures = [
        'tcc_control/fixtures/users.json',
        'tcc_control/fixtures/groups.json'
    ]

    @classmethod
    def setUpTestData(cls):
        teacher_group = Group.objects.get(id='3')
        cls.teacher = User.objects.get(id='7f7e4d1c-e707-4059-9d1a-27044afb6725')
        cls.participants = User.objects.exclude(groups=teacher_group)
        return super().setUpTestData()

    def test_description(self):
        data = {
            'description': '',
            'teacher': self.teacher,
            'participants': self.participants
        }
        form = TimetableForm(data=data)

        self.assertEqual(form.errors['description'], [Field.default_error_messages['required']])
