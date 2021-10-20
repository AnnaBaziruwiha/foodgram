from rest_framework import permissions


class CreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_authenticated()
        return False
