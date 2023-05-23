from rest_framework.response import Response
from rest_framework import status

from functools import wraps


def response(status_code, instance=None, detail=None, errors=None, serializer=None, many=False, **kwargs):
    """
    generate Response objects for API response
    """
    response_body = dict()
    if instance:
        if not serializer:
            raise Exception("serializer for instance not provided")
        serialized_instance = serializer(instance, many=many)
        response_body["instances"] = serialized_instance.data
    if detail:
        response_body["detail"] = detail
    if errors:
        response_body["errors"] = errors
    response_body.update(**kwargs)
    return Response(data=response_body, status=status_code)


def unauthorized():
    return response(status.HTTP_401_UNAUTHORIZED, detail="User inactive or deleted")


def obsolete(f):
    wraps(f)

    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


def logout(request):
    request.user.auth_token.delete()
    logout(request)
