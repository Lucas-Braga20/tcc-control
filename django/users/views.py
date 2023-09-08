"""
Views to users apps.
"""

from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import Http404

from users.forms import SignUpForm, ProfieForm
from users.models import User

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


class ProfileDetailView(NotificationMixin,
                        LoginRequiredMixin,
                        SuccessMessageMixin,
                        UpdateView,
                        View):
    """
    Profile view.
    """
    model = User
    form_class = ProfieForm
    template_name = 'registration/profile.html'
    success_message = 'Perfil atualizado com sucesso.'

    def get_success_url(self):
        instance = self.get_object()

        return instance.get_profile_url()

    def get_object(self):
        user_id = self.kwargs.get('pk')

        if not user_id != str(self.request.user.id):
            raise Http404('Você não tem permissão para acessar este perfil.')

        return self.request.user


class UserListView(NotificationMixin, GenericPermissionMixin, LoginRequiredMixin, TemplateView):
    """
    User List View.
    """
    template_name = 'users/list.html'
    required_groups = ['Professor da disciplina']
