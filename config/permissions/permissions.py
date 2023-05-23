from rest_framework.exceptions import PermissionDenied

from typing import List
from functools import wraps

from utils.permissions import get_req_and_kwarg

from utils.general import obsolete


@obsolete
def has_permissions(permissions: List[str]):
    # Do NOT USE
    """
    permission decorator for providing permission for each view and request.
    """

    def decorator(f):
        wraps(f)

        def wrapper(*args, **kwargs):
            request, pk = get_req_and_kwarg(args, kwargs, "pk")
            for permission in permissions:
                if not bool(getattr(request.user, permission)):
                    raise PermissionDenied
            return f(*args, **kwargs)

        return wrapper

    return decorator


def has_permission(request, filter_str, raise_exception=False):
    permission = bool(getattr(request.user, filter_str, False))
    if permission:
        return permission
    if raise_exception:
        raise PermissionDenied
    return permission


def has_obj_permission(request, obj=None, pk=None, raise_exception=False):
    permission: bool = False
    if pk and obj:
        raise ValueError("only pk or obj must get passed to function")
    if pk:
        permission = request.user.id == pk
    elif obj:
        permission = request.user.id == obj.id
    if permission:
        return permission
    if raise_exception:
        raise PermissionDenied
    return permission

