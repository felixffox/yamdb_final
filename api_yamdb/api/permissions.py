from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Разрешения для TitleViewSet, GenreViewSet, CategoryViewSet"""

    def is_admin_or_superuser(self, request):
        return request.user.is_admin or request.user.is_superuser

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and self.is_admin_or_superuser(request)))


class AdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """Разрешения для CommentViewSet,ReviewViewSet"""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.role == "moderator"
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
