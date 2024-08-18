from rest_framework import permissions


class IsAdminOrSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_superuser or request.user.is_admin)


class IsAuthorORIsAdminIModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or any(
                (
                    request.user.is_admin,
                    request.user.is_moderator,
                    request.user == obj.author,
                )
            )
        )
