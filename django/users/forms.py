"""
Implementação dos Formulários do app de usuários.

Contém os formulários para:
    - SignUpForm (Criação de conta);
    - ProfieForm (Perfil);
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class SignUpForm(UserCreationForm):
    """Formulário de cadastro de conta."""
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional',
    )
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional',
    )
    rgm = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(
        max_length=254, help_text='Enter a valid email address',
    )
    phone = forms.CharField(
        label='Telefone',
        widget=forms.TextInput(attrs={'placeholder': '(999) 9999-9999'}),
        help_text='Informe o número de telefone no formato (999) 9999-9999.'
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password1',
            'password2', 'phone', 'university_course',
        ]


class ProfieForm(forms.ModelForm):
    """Formulário de perfil do usuário."""

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'rgm', 'university_course', 'phone',
        ]
