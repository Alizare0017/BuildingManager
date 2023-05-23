from rest_framework import serializers

from .models import User
from utils.regex_validators import validators

from otp.models import OTP


class UserSerializer(serializers.ModelSerializer):
    is_manager = serializers.CharField(default=User.is_manager)
    is_resident = serializers.CharField(default=User.is_resident)

    class Meta:
        model = User
        exclude = ["user_permissions", "groups"]
        extra_kwargs = {"password": {"write_only": True}}


class _UserActionBase(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    username = serializers.CharField(validators=[validators.username])
    password = serializers.CharField(validators=[validators.password])


class RegisterUserSerializer(_UserActionBase):
    pass


class LoginSerializer(_UserActionBase):
    pass


class ChangeActiveStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=True)


class UpdateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(validators=[validators.phone], required=False)
    members = serializers.IntegerField(required=False, min_value=1)




