"""Implementação das Views do app de works.

Contém as telas para:
    - WorkStageView (Listagem de etapas);
    - WorkProposalListView (Listagem de propostas);
"""

from typing import Any
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, UpdateView, CreateView, View, ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.urls import reverse_lazy, reverse
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, Http404
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from works.models import FinalWorkVersion, FinalWork, FinalWorkStage
from works.forms import FinalWorkVersionForm, FinalWorkForm, FinalWorkCreateVersionForm

from users.models import User

from meetings.models import Meeting

from core.permissions import UserGroup, GenericPermissionMixin
from core.mixins import NotificationMixin
from core import defaults


class WorkStageView(NotificationMixin, LoginRequiredMixin, DetailView, View):
    """View genérica para etapas do TCC.

    Através desta view será implementado a tela de listagem de etapas do
    TCC. Implementando através da View Genérica: DetailView.

    Método suportado:
        - Retrieve;

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;
    """
    template_name = 'final-work-stages/list.html'
    model = FinalWork

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Método GET da rota."""
        user = self.request.user
        self.object = self.get_object()

        user_group = UserGroup(user=user)

        if user_group.is_supervisor() and user != self.object.supervisor:
            return HttpResponseForbidden(_('You do not belong to this TCC.'))

        if user_group.is_mentee() and not self.object.mentees.filter(id=user.id).exists():
            return HttpResponseForbidden(_('You do not belong to this TCC.'))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Gera o contexto da requisição."""
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()

        context['meetings'] = Meeting.objects.filter(work_stage__final_work=self.object).exclude(
            meeting_approved__approved=False
        ).exclude(
            meeting_approved__approved=None
        )
        context['work_stages'] = self.object.work_stage.order_by('stage__start_date')

        able_to_present = 'null'

        if self.object.able_to_present is True:
            able_to_present = 'true'
        elif self.object.able_to_present is False:
            able_to_present = 'false'

        context['able_to_present'] = able_to_present
        context['user_group'] = UserGroup(user=self.request.user)

        return context


class WorkMeetingsView(TemplateView):
    template_name = 'meetings/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        final_work_id = kwargs.get('pk')

        final_work = get_object_or_404(FinalWork, id=final_work_id)

        meetings = Meeting.objects.filter(work_stage__final_work=final_work).exclude(
            meeting_approved__approved=False
        ).exclude(
            meeting_approved__approved=None
        )

        context['final_work'] = final_work
        context['meetings'] = meetings
        context['total_meetings'] = meetings.count()

        return context


class WorkStageDevelopmentView(NotificationMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Work stage development view.
    """
    template_name = 'final-work-versions/editor.html'
    model = FinalWorkVersion
    form_class = FinalWorkVersionForm
    success_message = 'Trabalho salvo com sucesso.'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        stage = self.object.work_stage
        versions = stage.work_stage_version.all().order_by('created_at')
        if self.object != versions.last():
            return HttpResponseForbidden('This versions is blocked.')

        if stage.status in defaults.completed_status:
            return HttpResponseBadRequest('This stage already completed.')

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        object = self.get_object()

        stage = object.work_stage
        versions = stage.work_stage_version.all().order_by('created_at')
        context['versions'] = versions

        detail_object = context['object']
        context['fields'] = detail_object.work_stage.stage.activity_configuration.fields

        return context

    def get_success_url(self):
        return reverse('works:detail', kwargs={'pk': self.object.work_stage.id})


def create_work_stage_development(request):
    if request.method == 'POST':
        work_stage_id = request.POST.get('work_stage')

        if work_stage_id is None:
            return HttpResponseBadRequest()

        try:
            work_stage = FinalWorkStage.objects.get(id=work_stage_id)
        except:
            return Http404()

        form = FinalWorkCreateVersionForm(request.POST)
        if form.is_valid():
            version = form.save(commit=True)
            version.confirmed = True
            version.save()

            return redirect(reverse('works:development', kwargs={'pk': version.id}))
        else:
            return redirect(reverse('works:detail', kwargs={'pk': work_stage.id}) + '?error=true')

    return HttpResponseBadRequest()


class WorkStageDetailView(NotificationMixin, LoginRequiredMixin, DetailView, View):
    """
    Work stage detail screen.
    """
    template_name = 'final-work-stages/detail.html'
    model = FinalWorkStage

    def get(self, request, *args, **kwargs):
        error_param = request.GET.get('error')
        success_review_request = request.GET.get('success_review_request')
        success_mark_completed = request.GET.get('success_mark_completed')
        success_mark_presented = request.GET.get('success_mark_presented')
        success_change_request = request.GET.get('success_change_request')

        if success_review_request and success_review_request == 'true':
            messages.success(request, 'Correção solicitada com sucesso.')

            params = request.GET.copy()
            params.pop('success_review_request', None)
            querystring_without_error = params.urlencode()

            url_without_error = request.path + '?' + querystring_without_error
            return redirect(url_without_error)

        if success_mark_completed and success_mark_completed == 'true':
            messages.success(request, 'Atividade concluída com sucesso.')

            params = request.GET.copy()
            params.pop('success_mark_completed', None)
            querystring_without_error = params.urlencode()

            url_without_error = request.path + '?' + querystring_without_error
            return redirect(url_without_error)

        if success_mark_presented and success_mark_presented == 'true':
            messages.success(request, 'Atividade apresentada com sucesso.')

            params = request.GET.copy()
            params.pop('success_mark_presented', None)
            querystring_without_error = params.urlencode()

            url_without_error = request.path + '?' + querystring_without_error
            return redirect(url_without_error)

        if success_change_request and success_change_request == 'true':
            messages.success(request, 'Solicitação de alteração requisitada com sucesso.')

            params = request.GET.copy()
            params.pop('success_change_request', None)
            querystring_without_error = params.urlencode()

            url_without_error = request.path + '?' + success_change_request
            return redirect(url_without_error)

        if error_param and error_param == 'true':
            messages.error(request, 'Houve um erro no servidor. Tente novamente!')

            params = request.GET.copy()
            params.pop('error', None)
            querystring_without_error = params.urlencode()

            url_without_error = request.path + '?' + querystring_without_error
            return redirect(url_without_error)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.object = self.get_object()

        context['comments'] = self.object.stage_comment.all().order_by('created_at')
        context['meetings'] = self.object.stage_meeting.all().filter().order_by('-meeting_date')
        context['user_group'] = UserGroup(self.request.user)

        change_requests = self.object.work_stage_change_request.all().order_by('-created_at')

        if change_requests.exists():
            context['last_change_request'] = change_requests.first()
            context['change_already_requested'] = change_requests.first().approved == None
        else:
            context['change_already_requested'] = False

        return context


class WorkProposalCreateView(NotificationMixin, GenericPermissionMixin, LoginRequiredMixin, CreateView, View):
    """
    Work proposal create screen.
    """
    template_name = 'final-work-proposal/editor.html'
    model = FinalWork
    form_class = FinalWorkForm
    success_url = reverse_lazy('works:proposal-list')
    success_message = 'Proposta de TCC criada com sucesso.'
    required_groups = ['Orientando']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class WorkProposalListView(NotificationMixin, LoginRequiredMixin, ListView, View):
    """View genérica para propostas de TCC.

    Através desta view será implementado a tela de listagem de propostas de
    TCC. Implementando através da View Genérica: ListView.

    Método suportado:
        - List;

    Permissões necessárias:
        - Autenticação: Apenas poderá consumir endpoint mediante autenticação;

    Perfis:
        - Professor: Visualiza todas as propostas;
        - Orientador: Visualiza apenas as propostas que orienta;
        - Orientando: Visualiza apenas as suas propostas;
    """
    template_name = 'final-work-proposal/list.html'
    model = FinalWork

    def get_queryset(self):
        """Processa queryset."""
        queryset = super().get_queryset()

        user_group = UserGroup(self.request.user)

        if user_group.is_mentee():
            queryset = queryset.filter(mentees__in=[self.request.user])

        if user_group.is_supervisor():
            queryset = queryset.filter(supervisor=self.request.user)

        queryset = queryset.exclude(archived=True)

        return queryset

    def get_context_data(self, **kwargs):
        """Gera o contexto da requisição."""
        context = super().get_context_data(**kwargs)

        context['user_group'] = UserGroup(self.request.user)
        context['supervisor'] = User.objects.filter(groups__name='Orientador')
        context['mentee_group'] = Group.objects.get(name='Orientando')
        context['teacher_group'] = Group.objects.get(name='Professor da disciplina')
        context['allow_create'] = not FinalWork.objects.filter(
            mentees__in=[self.request.user]
        ).exclude(archived=True).exists()

        return context


class WorkListView(NotificationMixin, GenericPermissionMixin, LoginRequiredMixin, TemplateView):
    """
    Final work list screen.
    """
    template_name = 'final-work/list.html'
    required_groups = ['Orientador', 'Professor da disciplina']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        user_group = UserGroup(user)

        context['teacher'] = user_group.is_teacher()

        return context


class ChangeRequestListView(NotificationMixin, GenericPermissionMixin, LoginRequiredMixin, TemplateView):
    """
    Change request list view.
    """
    template_name = 'change-requests/list.html'
    required_groups = ['Professor da disciplina']
