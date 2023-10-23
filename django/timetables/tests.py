"""
Implementação dos Testes do app de timetables.

Contém os testes para:
    - TimetableTest (Cronograma);
    - StageTest (Etapas);
"""

import datetime

from django.test import TestCase
from django.contrib.auth.models import Group
from django.forms.fields import Field
from django.core.files.uploadedfile import SimpleUploadedFile

from activities.models import ActivityConfiguration

from timetables.forms import TimetableForm, StageForm
from timetables.serializers import StageSerializer

from users.models import User


class TimetableTest(TestCase):
    """Teste de Timetable."""

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
        """Testa a descrição do cronograma."""

        data = {
            'description': '',
            'teacher': self.teacher,
            'participants': self.participants
        }
        form = TimetableForm(data=data)

        self.assertEqual(form.errors['description'], [Field.default_error_messages['required']])

    def test_teacher(self):
        """Teste de integração de professor.

        Verifica se o professor do tcc possui perfil de professor.
        """
        data = {
            'description': '',
            'teacher': self.participants.first(),
            'participants': self.participants,
        }
        form = TimetableForm(data=data)

        self.assertEqual(form.errors['teacher'], ['Faça uma escolha válida. Sua escolha não é uma das disponíveis.'])

    def test_participants(self):
        """Teste de integração de participantes.

        Verifica se os participantes possuem perfil de
        orientandos ou orientadores.
        """
        data = {
            'description': 'Cronograma correto.',
            'teacher': self.teacher,
            'mentee_field': self.users.filter(groups__name='Orientando'),
            'supervisor_field': self.users.filter(groups__name='Orientador'),
        }
        files = {
            'document_template': SimpleUploadedFile('arquivo.docx', b'Teste'),
        }
        form = TimetableForm(data=data, files=files)

        self.assertTrue(form.is_valid())


class StageTest(TestCase):
    """Teste de Stage."""

    fixtures = [
        'tcc_control/fixtures/courses.json',
        'tcc_control/fixtures/users.json',
        'tcc_control/fixtures/groups.json',
        'tcc_control/fixtures/timetables.json',
        'tcc_control/fixtures/tests/activity_configurations.json',
    ]

    @classmethod
    def setUpTestData(cls):
        cls.activity_configuration = ActivityConfiguration.objects.get(id='276d009c-8c9e-4f05-894c-893ab496335b')
        return super().setUpTestData()

    def test_description(self):
        """Testa o campo descrição."""
        form_data = {
            'description': '',
            'start_date': datetime.date.today(),
            'send_date_supervisor': datetime.date.today() + datetime.timedelta(days=1),
            'send_date': datetime.date.today() + datetime.timedelta(days=2),
            'activity_configuration': self.activity_configuration
        }
        serializer_data = {
            'description': '',
            'start_date': datetime.date.today(),
            'send_date_supervisor': datetime.date.today() + datetime.timedelta(days=1),
            'send_date': datetime.date.today() + datetime.timedelta(days=2),
            'activity_configuration': self.activity_configuration.id,
        }

        form = StageForm(data=form_data)

        serializer = StageSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())

        serializer_errors = [str(error) for error in serializer.errors.get('description')]

        self.assertEqual(form.errors['description'], [Field.default_error_messages['required']])
        self.assertIn('Este campo não pode ser em branco.', serializer_errors)

    def test_dates(self):
        """Testa os campos do tipo datetime."""
        form_data = {
            'description': 'Teste',
            'start_date': '2023-02-30',
            'send_date_supervisor': '2023-03-01',
            'send_date': '2023-03-02',
            'activity_configuration': self.activity_configuration,
        }
        serializer_data = {
            'description': 'Teste',
            'start_date': '2023-02-30',
            'send_date_supervisor': '2023-03-01',
            'send_date': '2023-03-02',
            'activity_configuration': self.activity_configuration.id,
        }

        form = StageForm(data=form_data)

        serializer = StageSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())

        serializer_errors = [str(error) for error in serializer.errors.get('start_date')]

        self.assertEqual(form.errors['start_date'], ['Informe uma data válida.'])
        self.assertIn('Formato inválido para data. Use um dos formatos a seguir: YYYY-MM-DD.', serializer_errors)

    def test_date_order(self):
        """Testa a ordem dos campos do tipo datetime."""
        today = datetime.date.today()

        form_data = {
            'description': 'Teste',
            'start_date': today + datetime.timedelta(days=3),
            'send_date_supervisor': today + datetime.timedelta(days=1),
            'send_date': today + datetime.timedelta(days=1),
            'activity_configuration': self.activity_configuration,
        }
        serializer_data = {
            'description': 'Teste',
            'start_date': today + datetime.timedelta(days=3),
            'send_date_supervisor': today + datetime.timedelta(days=1),
            'send_date': today + datetime.timedelta(days=1),
            'activity_configuration': self.activity_configuration.id,
            'timetable': 'a90dd479-de02-440f-94e3-d6af553af551',
        }

        form = StageForm(data=form_data)

        serializer = StageSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())

        serializer_errors = [str(error) for error in serializer.errors.get('start_date')]

        self.assertEqual(form.errors['start_date'], ['A data de envio ao supervisor deve ser após a data de início'])
        self.assertIn('A data de envio ao supervisor deve ser após a data de início', serializer_errors)

    def test_date_advisor_order(self):
        """Testa a ordem da data de envio ao orientador."""
        today = datetime.date.today()

        form_data = {
            'description': 'Teste',
            'start_date': today + datetime.timedelta(days=1),
            'send_date_supervisor': today + datetime.timedelta(days=3),
            'send_date': today + datetime.timedelta(days=1),
            'presentation_date': today + datetime.timedelta(days=1),
            'activity_configuration': self.activity_configuration,
        }

        serializer_data = {
            'description': 'Teste',
            'start_date': today + datetime.timedelta(days=1),
            'send_date_supervisor': today + datetime.timedelta(days=3),
            'send_date': today + datetime.timedelta(days=1),
            'presentation_date': today + datetime.timedelta(days=1),
            'activity_configuration': self.activity_configuration.id,
            'timetable': 'a90dd479-de02-440f-94e3-d6af553af551',
        }

        form = StageForm(data=form_data)

        serializer = StageSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())

        serializer_errors = [str(error) for error in serializer.errors.get('send_date_supervisor')]

        self.assertEqual(form.errors['send_date_supervisor'], [
            'A data de envio ao orientador deve ser antes da data de envio.'
        ])

        self.assertIn('A data de envio ao orientador deve ser antes da data de envio.', serializer_errors)
