"""
Views to users apps.
"""

from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group

from users.forms import SignUpForm

from core.permissions import GenericPermissionMixin
from core.mixins import NotificationMixin


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        group = Group.objects.get(name='Orientando')

        instance = form.save()
        instance.groups.add(group)

        return super().form_valid(form)


class UserListView(NotificationMixin, GenericPermissionMixin, LoginRequiredMixin, TemplateView):
    """
    User List View.
    """
    template_name = 'users/list.html'
    required_groups = ['Professor da disciplina']
