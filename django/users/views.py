"""
Views to users apps.
"""

from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from users.forms import SignUpForm

from core.permissions import GenericPermissionMixin


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class UserListView(GenericPermissionMixin, LoginRequiredMixin, TemplateView):
    """
    User List View.
    """
    template_name = 'users/list.html'
    required_groups = ['Professor da disciplina']
