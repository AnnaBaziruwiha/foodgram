from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and (
                request.user == obj.user or request.user == obj.author
            )
        )


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'
