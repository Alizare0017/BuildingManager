from rest_framework import serializers

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class MangerNewTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ["building", "from_user", "to_user", "title", "message"]
        read_only_fields = ["from_user"]


class ResidentNewTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["title", "message"]
