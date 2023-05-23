from rest_framework import serializers

from .models import Bill
from buildings.models import Unit


class BillSerializer(serializers.ModelSerializer):
    is_overdue = serializers.BooleanField(default="is_overdue")

    class Meta:
        model = Bill
        fields = "__all__"
        # read_only_fields = ["created_by", "date_created", "is_paid", "amount", "expire_date"]


class NewBillSerializer(serializers.Serializer):
    MEMBER = "member"
    UNIT = "unit"

    amount = serializers.FloatField()
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all(), required=False)
    divide_by = serializers.ChoiceField(choices=(MEMBER, UNIT), required=False)
    expire_date = serializers.IntegerField()
    description = serializers.CharField()

