from rest_framework import serializers

from advertisements.models import Advertisement
from buildings.models import Unit


class AdOutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertisement
        fields = "__all__"
        depth = 2


class AdInSerializer(serializers.ModelSerializer):
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())


    """
    This is a validation function for the AdInSerializer serializer class. It checks if the provided data dictionary contains the required fields depending on the value of the what_for field.

    If the what_for field is set to Advertisement.RENT, then the function checks if the rent field is present in the data dictionary. If it's not present, the function raises a serializers.ValidationError with the message "rent amount is necessary".

    If the what_for field is set to Advertisement.SALE, then the function checks if the price field is present in the data dictionary. If it's not present, the function raises a serializers.ValidationError with the message "price amount is necessary".

    The function then returns the original data dictionary if everything is valid.
    """
    class Meta:
        model = Advertisement
        exclude = ["unit_specification"]

    def validate(self, data):
        if data["what_for"] == Advertisement.RENT:
            if not data.get("rent"):
                raise serializers.ValidationError(detail="rent amount is necessary")
        elif data["what_for"] == Advertisement.SALE:
            if not data.get("price"):
                raise serializers.ValidationError(detail="price amount is necessary")
        return data
