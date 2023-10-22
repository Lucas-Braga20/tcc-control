"""
Implementação dos ViewSets do app de comentários.

Contém os endpoints para:
    - CommentViewSet (Comentários);
"""

from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter

from comments.models import Comment
from comments.serializers import CommentSerializer

from core.permissions import UserGroup

from django_filters.rest_framework import DjangoFilterBackend


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet para manipulação de comentários.

    Através deste endpoint que será possível manipular
    comentários.

    Métodos suportados:
        - Retrieve;
        - List;
        - Update;
        - Create;
        - Delete;

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    model = Comment
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['work_stage']

    def get_queryset(self):
        """Recupera o queryset de comentários."""
        queryset = super().get_queryset()

        user_group = UserGroup(self.request.user)

        if user_group.is_supervisor():
            queryset = queryset.filter(work_stage__final_work__supervisor=self.request.user)

        if user_group.is_mentee():
            queryset = queryset.filter(work_stage__final_work__mentees__in=[self.request.user])

        if user_group.is_teacher():
            queryset = queryset.filter(work_stage__final_work__timetable__teacher=self.request.user)

        no_page = self.request.query_params.get('no_page')
        if no_page:
            self.pagination_class = None

        queryset = queryset.order_by('created_at')

        return queryset
