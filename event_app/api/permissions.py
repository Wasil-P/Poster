from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUserOrRegister(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return bool(request.user and request.user.is_superuser)


class IsAuthenticatedOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST" and request.user and request.user.is_authenticated:
            return True
        return bool(request.method in SAFE_METHODS)