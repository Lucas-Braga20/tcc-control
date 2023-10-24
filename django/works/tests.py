"""Testes do app de works."""

import datetime

from django.test import TestCase

from works.forms import FinalWorkVersionForm, FinalWorkStageForm
from works.models import FinalWorkStage, ChangeRequest, FinalWorkVersion

from core.defaults import WORK_STAGE_COMPLETED, WORK_STAGE_PRESENTED


class FinalWorkStageTest(TestCase):
    """Testes do TCC."""

    fixtures = [
        'tcc_control/fixtures/courses.json',
        'tcc_control/fixtures/users.json',
        'tcc_control/fixtures/activity_configurations.json',
        'tcc_control/fixtures/timetables.json',
        'tcc_control/fixtures/stages.json',
        'tcc_control/fixtures/final_works.json',
        'tcc_control/fixtures/final_work_stages.json',
    ]

    @classmethod
    def setUpTestData(cls):
        cls.final_work_stage = FinalWorkStage.objects.get(id='571926b8-5eb1-48d8-922a-ab2fcdb92ac4')
        return super().setUpTestData()

    def test_finish_stage(self):
        """Teste de integração de etapa do TCC.

        Esse teste verifica se só será possível marcar como concluído
        uma etapa que possuir pelo menos um desenvolvimento.
        """
        data = {
            'status': WORK_STAGE_COMPLETED,
        }
        form = FinalWorkStageForm(data=data, instance=self.final_work_stage)

        self.assertEqual(
            form.errors['status'],
            ['Só será possível marcar como completado se houver um desenvolvimento.'],
        )

    def test_presented_stage(self):
        """Teste de integração de apresentação de etapa.

        Teste de integração usado para verificar se só será
        será possível marcar uma atividade como "apresentada" quando
        a data de hoje é igual ou posterior à data de apresentação.
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
            self.assertEqual(
                form.errors.get('status'),
                ['Só é possível marcar como apresentado se hoje for a data ou posterior.'],
            )


class FinalWorkVersionTest(TestCase):
    """Testes do versão do TCC."""

    fixtures = [
        'tcc_control/fixtures/courses.json',
        'tcc_control/fixtures/users.json',
        'tcc_control/fixtures/activity_configurations.json',
        'tcc_control/fixtures/timetables.json',
        'tcc_control/fixtures/stages.json',
        'tcc_control/fixtures/final_works.json',
        'tcc_control/fixtures/final_work_stages.json',
        'tcc_control/fixtures/versions.json',
    ]

    @classmethod
    def setUpTestData(cls):
        cls.first_version = FinalWorkVersion.objects.get(id='4290ea3d-49d7-4c0b-8d63-24724dc77175')
        cls.second_version = FinalWorkVersion.objects.get(id='123a9e57-c204-417b-be8b-429d5de22c7a')
        return super().setUpTestData()

    def test_contents(self):
        """Teste de integração de conteúdo da versão.

        Teste de integração usado para verificar se a versão
        contém os campos estruturados de forma correta com key/value.
        """
        form = FinalWorkVersionForm(instance=self.first_version, data={
            'content': {
                'fields': [
                    {
                        'key': 'resumo',
                    }
                ],
            },
        })

        self.assertFalse(form.is_valid())

        self.assertEqual(form.errors['content'], ['Um campo não foi inserido corretamente.'])

    def test_contents_keys(self):
        """Teste de integração de keys do conteúdo da versão.

        Teste de integração usado para verificar se a versão
        contém os campos com keys corretas baseados na atividade.
        """
        form = FinalWorkVersionForm(instance=self.second_version, data={
            'content': {
                'fields': [
                    {
                        'key': 'titulo_errado',
                        'value': '',
                    }
                ]
            },
        })

        self.assertFalse(form.is_valid())

        self.assertEqual(form.errors['content'], ['O conteúdo da atividade contém campos inválidos.'])


class ChangeRequestTest(TestCase):
    """Teste de pedido de alteração."""

    fixtures = [
        'tcc_control/fixtures/courses.json',
        'tcc_control/fixtures/users.json',
        'tcc_control/fixtures/activity_configurations.json',
        'tcc_control/fixtures/timetables.json',
        'tcc_control/fixtures/stages.json',
        'tcc_control/fixtures/final_works.json',
        'tcc_control/fixtures/final_work_stages.json',
        'tcc_control/fixtures/tests/change_requests.json',
    ]

    @classmethod
    def setUpTestData(cls):
        cls.change_request = ChangeRequest.objects.get(id='5827bbbc-b6f8-4bdb-92cc-70e8916422f9')
        return super().setUpTestData()

    def test_approve_request(self):
        """Teste de integração para aprovar pedido de alteração.

        Esse teste de integração irá verificar se ao aprovar um pedido
        uma nova versão será criada.
        """
        self.change_request.approve_request()
        self.assertEqual(FinalWorkVersion.objects.all().count(), 1)
