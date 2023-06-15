"""
Forms to comments app.
"""

from django import forms

from comments.models import Comment


class CommentForm(forms.ModelForm):
    """
    Comment form.
    """

    class Meta:
        model = Comment
        fields = '__all__'

    def clean(self):
        author = self.cleaned_data.get('author')
        work_stage = self.cleaned_data.get('work_stage')

        if author and work_stage:
            supervisor = work_stage.final_work.supervisor
            mentees = work_stage.final_work.mentees.all()

            is_mentee = mentees.filter(id=author.id).exists()
            is_supervisor = author.id == supervisor.id

            if not is_supervisor or not is_mentee:
                raise forms.ValidationError({'author': 'The comment can only be made by a TCC member.'})
