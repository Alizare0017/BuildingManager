from .models import Building, Unit, UnitSpecification

from users.models import User

from rest_framework import serializers


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = "__all__"


class BuildingBaseSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CreateBuildingSerializer(BuildingBaseSerializer):
    name = serializers.CharField(max_length=20)

    unit_count = serializers.IntegerField(max_value=50)


class UpdateBuildingSerializer(BuildingBaseSerializer):
    name = serializers.CharField(max_length=20, required=False)

    address = serializers.CharField(required=False)


class UnitSerializer(serializers.ModelSerializer):
    resident_full_name = serializers.CharField(source="resident.get_full_name", default=None)

    class Meta:
        model = Unit
        fields = "__all__"


class ResidentSerializer(serializers.ModelSerializer):
    resident_full_name = serializers.CharField(source="full_name")

    class Meta:
        model = User
        fields = ["username", "resident_full_name", "email", "phone"]


class UnitSpecificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnitSpecification
        fields = "__all__"

