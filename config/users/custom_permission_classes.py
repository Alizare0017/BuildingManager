from rest_framework.permissions import BasePermission

from permissions import filters


class ListUserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            return bool(getattr(request.user, filters.IS_STAFF))
        return True


class DestroyUserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == "DELETE":
            return bool(getattr(request.user, filters.IS_STAFF))
        return True


class ChangeActiveStatusPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(getattr(request.user, filters.IS_STAFF))
