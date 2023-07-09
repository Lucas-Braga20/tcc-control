"""
Permissions config to TCC Control app.
"""

from rest_framework import permissions

from django.contrib.auth.models import Group
from django.contrib.auth.mixins import AccessMixin


class RoleAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        roles_required = getattr(view, 'roles_required', [])
        user_role = request.user.groups.all().first()

        if request.user.is_superuser:
            return True

        if roles_required and user_role.name in roles_required:
            return True
        return False


class GenericPermissionMixin(AccessMixin):
    required_groups = []

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission(request):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self, request):
        if not self.required_groups:
            raise NotImplementedError("The 'required_groups' attribute must be set with at least one group.")

        user_groups = request.user.groups.values_list('name', flat=True)
        return any(group in user_groups for group in self.required_groups)


class UserGroup:
    user = None

    def __init__(self, user):
        self.user = user

    def is_mentee(self):
        if not self.user:
            return None

        self.mentee = Group.objects.get(id=2)

        return self.user.groups.first() == self.mentee

    def is_supervisor(self):
        if not self.user:
            return None

        self.supervisor = Group.objects.get(id=1)

        return self.user.groups.first() == self.supervisor

    def is_teacher(self):
        if not self.user:
            return None

        self.teacher = Group.objects.get(id=3)

        return self.user.groups.first() == self.teacher
