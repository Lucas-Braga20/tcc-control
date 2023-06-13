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
        work_step = self.cleaned_data.get('work_step')

        if author and work_step:
            advisor = work_step.tcc_work.advisor
            advised = work_step.tcc_work.advised.all()

            is_advised = advised.filter(id=author.id).exists()
            is_advisor = author.id == advisor.id

            if not is_advised or not is_advisor:
                raise forms.ValidationError({'author': 'The comment can only be made by a TCC member.'})
