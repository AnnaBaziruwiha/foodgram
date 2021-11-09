from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user == obj.user or (
            request.method == 'POST'
        ):
            return True
        return request.method in permissions.SAFE_METHODS


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user == obj.author or (
            request.method == 'POST'
        ):
            return True
        return request.method in permissions.SAFE_METHODS
