"""
Implementação dos Formulários do app de comments.

Contém os formulários para:
    - CommentForm (Comentários);
"""

from django import forms

from comments.models import Comment


class CommentForm(forms.ModelForm):
    """Formulário de comentário."""

    class Meta:
        model = Comment
        fields = '__all__'

    def clean(self):
        """Validação dos campos.

        Apenas é possível criar um comentário se o usuário
        for membro do TCC.

        Está validação é feita a partir do campo work stage.
        """
        author = self.cleaned_data.get('author')
        work_stage = self.cleaned_data.get('work_stage')

        if author and work_stage:
            supervisor = work_stage.final_work.supervisor
            mentees = work_stage.final_work.mentees.all()

            is_mentee = mentees.filter(id=author.id).exists()
            is_supervisor = author.id == supervisor.id
            is_teacher = author.id == work_stage.final_work.timetable.teacher

            if not is_supervisor or not is_mentee or not is_teacher:
                raise forms.ValidationError({'author': 'O comentário só pode ser feito por um membro do TCC.'})
