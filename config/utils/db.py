from users.models import User

from buildings.models import Unit

from .exceptions import BadRequest


def update_instance(instance, validated_data):
    for data in validated_data:
        new_data = validated_data[data]
        if getattr(instance, data) == new_data:
            continue
        setattr(instance, data, new_data)
        if isinstance(instance, User):
            if data == "email":
                setattr(instance, "is_email_activated", False)
            if data == "phone":
                setattr(instance, "is_phone_activated", False)
    instance.save()
    instance.refresh_from_db()
    return instance


def update_unit_member(request, members):
    if request.user.is_manager:
        raise BadRequest(detail="managers cant set members field")
    user_unit = Unit.objects.filter(resident=request.user).first()
    update_instance(user_unit, {"members": members})
