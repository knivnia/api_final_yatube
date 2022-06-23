from rest_framework import exceptions, permissions


class UserIsAuthor(permissions.BasePermission):
    """Permission for author to edit his content."""

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return request.user == obj.author
        return True


class MethodsAndIsAdminUser(permissions.BasePermission):
    """Permission for admin to create, change and delete groups."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True
        raise exceptions.MethodNotAllowed(request.method)
