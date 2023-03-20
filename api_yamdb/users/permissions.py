from rest_framework import permissions


class RoleAdmin(permissions.BasePermission):
    """Админские права (role=admin)"""

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == "admin":
            return True
        else:
            return None
