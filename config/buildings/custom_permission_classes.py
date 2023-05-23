from rest_framework.permissions import BasePermission

from permissions import filters


class IsStaffOrManager(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return bool(getattr(request.user, filters.IS_STAFF))
        if request.method == "POST":
            return bool(getattr(request.user, filters.IS_MANAGER))


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(getattr(request.user, filters.IS_MANAGER))
