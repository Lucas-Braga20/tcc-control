"""
Permissions config to TCC Control app.
"""

from rest_framework import permissions


class RoleAccessPermission(permissions.BasePermission):
    role_required = []

    def has_permission(self, request, view):
        roles_required = getattr(self, 'roles_required', [])
        user_role = request.user.groups.all().first()

        if request.user.is_superuser:
            return True

        if roles_required and user_role.name in roles_required:
            return True
        return False
