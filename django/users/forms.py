"""
Forms to users app.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class SignUpForm(UserCreationForm):
    """
    Sign up form.
    """
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    rgm = forms.CharField(max_length=20, required=True)
    university_course = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')
    phone = forms.CharField(
        label='Telefone',
        widget=forms.TextInput(attrs={'placeholder': '(999) 9999-9999'}),
        help_text='Informe o número de telefone no formato (999) 9999-9999.'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'phone',
        ]


class ProfieForm(forms.ModelForm):
    """
    Profile form.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'rgm', 'university_course', 'phone']
