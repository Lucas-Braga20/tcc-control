"""Implementação dos ViewSets do app de meetings.

Contém os endpoints para:
    - Meetings (Reuniões);
"""

from rest_framework import mixins, permissions, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from meetings.models import Meeting
from meetings.serializers import MeetingSerializer

from notifications.utils import send_notification


class MeetingViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    """ViewSet para manipulação de objetos Meetings.

    Através deste endpoint que todos os usuários poderão solicitar
    reuniões e aprová-las ou reprová-las.

    Métodos suportados:
        - Create;
        - Retrieve;
        - List;

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;

    Ações customizadas:
        - Approve: Aprova uma reunião solicitada;
        - Disapprove: Reprova uma reunião solicitada;
    """
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    model = Meeting
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Processa queryset."""
        queryset = super().get_queryset()

        no_page = self.request.query_params.get('no_page')
        if no_page:
            self.pagination_class = None

        queryset = queryset.order_by('-meeting_date')

        return queryset

    @action(methods=['post'], detail=False)
    def approve(self, request, **kwargs):
        """Ação de aprovação."""
        meeting_id = self.request.data.get('meeting')

        if meeting_id is None:
            return Response(data={'meeting': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            meeting = Meeting.objects.get(id=meeting_id)
        except:
            return Response(data={'meeting': 'Meeting not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = self.request.user

        review = meeting.meeting_approved.all().filter(user=user)

        if review.exists() is False:
            return Response(data={'meeting': 'You are not included in this meeting.'},
                            status=status.HTTP_404_NOT_FOUND)

        review = review.first()
        review.approved = True
        review.save()

        if not meeting.meeting_approved.exclude(approved=True).exists():
            send_notification(
                description=f'A reunião: "{meeting.description}", foi aprovada.',
                author=None,
                receivers=list(meeting.participants.all())
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False)
    def disapprove(self, request, **kwargs):
        """Ação de reprovação."""
        meeting_id = self.request.data.get('meeting')

        if meeting_id is None:
            return Response(data={'meeting': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            meeting = Meeting.objects.get(id=meeting_id)
        except:
            return Response(data={'meeting': 'Meeting not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = self.request.user

        review = meeting.meeting_approved.all().filter(user=user)
        already_disapproved = meeting.get_is_approved() == False

        if review.exists() is False:
            return Response(data={'meeting': 'You are not included in this meeting.'},
                            status=status.HTTP_404_NOT_FOUND)

        review = review.first()
        review.approved = False
        review.save()

        if not already_disapproved and meeting.get_is_approved() == False:
            send_notification(
                description=f'A reunião: "{meeting.description}", foi reprovada.',
                author=None,
                receivers=list(meeting.participants.all())
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
