"""Testes do app de comments."""

from django.test import TestCase

from rest_framework.test import APIRequestFactory

from works.models import FinalWorkStage

from users.models import User

from comments.forms import CommentForm
from comments.serializers import CommentSerializer


class CommentTest(TestCase):
    """Testes de comentário."""
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
        cls.final_work_stage = FinalWorkStage.objects.get(id='15f64554-efa0-4a6a-bf1d-b01463ac75dc')
        cls.user = User.objects.get(id='8bbc2d21-8d8c-436e-bcd1-140391155e0e')
        return super().setUpTestData()

    def test_author(self):
        """Testa o autor do comentário.

        Apenas é possível implementar um comentário se o autor
        for integrante do comentário.
        """
        factory = APIRequestFactory()

        request = factory.get('/api/comments')
        request.user = self.user

        form_data = {
            'description': 'Comentário feito por uma pessoa de fora do TCC.',
            'work_stage': self.final_work_stage,
            'author': self.user,
        }

        serializer_data = {
            'description': 'Comentário feito por uma pessoa de fora do TCC.',
            'work_stage': self.final_work_stage.id,
            'author': self.user,
        }

        form = CommentForm(data=form_data)
        serializer = CommentSerializer(data=serializer_data, context={'request': request})

        self.assertFalse(serializer.is_valid())

        self.assertEqual(form.errors['author'], ['O comentário só pode ser feito por um membro do TCC.'])
        self.assertIn('O comentário só pode ser feito por um membro do TCC.', serializer.errors.get('work_stage'))
