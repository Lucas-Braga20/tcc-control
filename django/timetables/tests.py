"""
Tests for timetables app.
"""

import datetime

from django.test import TestCase
from django.contrib.auth.models import Group
from django.forms.fields import Field

from activities.models import ActivityConfiguration

from timetables.forms import TimetableForm, StageForm

from users.models import User


class TimetableTest(TestCase):
    """
    Timetable test.
    """
    fixtures = [
        'tcc_control/fixtures/courses.json',
        'tcc_control/fixtures/users.json',
        'tcc_control/fixtures/groups.json'
    ]

    @classmethod
    def setUpTestData(cls):
        teacher_group = Group.objects.get(id='3')
        cls.teacher = User.objects.get(id='7f7e4d1c-e707-4059-9d1a-27044afb6725')
        cls.participants = User.objects.exclude(groups=teacher_group)
        cls.users = User.objects.all()
        return super().setUpTestData()

    def test_description(self):
        data = {
            'description': '',
            'teacher': self.teacher,
            'participants': self.participants
        }
        form = TimetableForm(data=data)

        self.assertEqual(form.errors['description'], [Field.default_error_messages['required']])

    def test_teacher(self):
        """
        Integration test to verify that the teacher is a
        user with the teacher profile.
        """
        data = {
            'description': '',
            'teacher': self.participants.first(),
            'participants': self.participants
        }
        form = TimetableForm(data=data)

        self.assertEqual(form.errors['teacher'], ['Esse campo deve conter um usuário com perfil de professor.'])

    def test_participants(self):
        """
        Integration test to verify if the participants
        have the profile of mentors or mentees.
        """
        data = {
            'description': '',
            'teacher': self.teacher,
            'participants': self.users
        }
        form = TimetableForm(data=data)

        self.assertEqual(form.errors['participants'], ['Participants must have the profile of mentors or mentees.'])


class StageTest(TestCase):
    """
    Stage test.
    """
    fixtures = [
        'tcc_control/fixtures/courses.json',
        'tcc_control/fixtures/users.json',
        'tcc_control/fixtures/groups.json',
        'tcc_control/fixtures/tests/activity_configurations.json'
    ]

    @classmethod
    def setUpTestData(cls):
        cls.activity_configuration = ActivityConfiguration.objects.get(id='276d009c-8c9e-4f05-894c-893ab496335b')
        return super().setUpTestData()

    def test_description(self):
        data = {
            'description': '',
            'start_date': datetime.date.today(),
            'send_date_supervisor': datetime.date.today() + datetime.timedelta(days=1),
            'send_date': datetime.date.today() + datetime.timedelta(days=2),
            'activity_configuration': self.activity_configuration
        }
        form = StageForm(data=data)

        self.assertEqual(form.errors['description'], [Field.default_error_messages['required']])

    def test_dates(self):
        data = {
            'description': 'Teste',
            'start_date': '2023-02-30',
            'send_date_supervisor': '2023-03-01',
            'send_date': '2023-03-02',
            'activity_configuration': self.activity_configuration
        }
        form = StageForm(data=data)

        self.assertEqual(form.errors['start_date'], ['Enter a valid date.'])

    def test_date_order(self):
        data = {
            'description': 'Teste',
            'start_date': '2023-03-03',
            'send_date_supervisor': '2023-03-01',
            'send_date': '2023-03-02',
            'activity_configuration': self.activity_configuration
        }
        form = StageForm(data=data)

        self.assertEqual(form.errors['start_date'], ['A data de envio ao supervisor deve ser após a data de início.'])

    def test_date_advisor_order(self):
        data = {
            'description': 'Teste',
            'start_date': '2023-02-28',
            'send_date_supervisor': '2023-03-03',
            'send_date': '2023-03-02',
            'presentation_date': '2023-03-01',
            'activity_configuration': self.activity_configuration
        }
        form = StageForm(data=data)

        self.assertEqual(form.errors['send_date_supervisor'], [
            'A data de envio ao orientador deve ser antes da data de envio'
        ])
