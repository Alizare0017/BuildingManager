from rest_framework import serializers

from .models import OTP


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = "__all__"

class OTPBaseSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    otp_for = serializers.ChoiceField(choices=OTP.type_choices)


class SendOTPSerializer(OTPBaseSerializer):
    pass


class OTPVerificationSerializer(OTPBaseSerializer):
    otp = serializers.IntegerField(max_value=999999)