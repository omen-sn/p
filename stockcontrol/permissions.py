from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Власники або адміністратори можуть оновлювати або видаляти
        return obj.user == request.user or request.user.is_staff

class CustomPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it,
    authenticated users to create, and anyone to read.
    """

    def has_permission(self, request, view):
        # Allow create actions for authenticated users
        if request.method == 'POST':
            return request.user.is_authenticated
        # Allow read actions for any request
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the object or an admin
        return obj.user == request.user or request.user.is_staff