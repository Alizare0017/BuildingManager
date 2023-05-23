from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView

from users.models import User
from .models import Ticket
from . import serializers as cs

from buildings.models import Building
from buildings.custom_permission_classes import IsManager

from permissions.permissions import has_obj_permission


from utils.general import response


class ManagerTicketView(APIView):
    permission_classes = [IsManager]

    def get(self, request, pk):
        building = get_object_or_404(Building, pk=pk)
        has_obj_permission(request, obj=building.owner, raise_exception=True)
        tickets = Ticket.objects.filter(building=building, to_user=request.user)
        return response(status.HTTP_200_OK, instance=tickets, serializer=cs.TicketSerializer, many=True)


class TicketsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        for residents to see their inbox. managers can use ManagersTicketView to see all tickets for their building
        """
        if request.user.is_manager:
            return response(status.HTTP_400_BAD_REQUEST, detail="use buildings tickets view")
        inbox_tickets = Ticket.objects.filter(to_user=request.user, building__units__resident=request.user)
        return response(status.HTTP_200_OK, instance=inbox_tickets, serializer=cs.TicketSerializer, many=True)

    def post(self, request):

        if request.user.is_resident:
            serializer = cs.ResidentNewTicketSerializer(data=request.data)
            if not serializer.is_valid():
                return response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
            building = Building.objects.filter(units__resident=request.user).first()
            to_user = building.owner
            ticket = Ticket.objects.create(
                to_user=to_user, from_user=request.user,
                building=building,
                **serializer.data)
            return response(status.HTTP_201_CREATED, instance=ticket, serializer=cs.TicketSerializer)

        elif request.user.is_manager:
            serializer = cs.MangerNewTicketSerializer(data=request.data)
            if not serializer.is_valid():
                return response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
            data = serializer.data
            if not Building.objects.filter(units__resident=data["to_user"]).exists():
                return response(status.HTTP_400_BAD_REQUEST, detail="user is not for this building")
            building = get_object_or_404(Building, pk=data["building"])
            to_user = get_object_or_404(User, pk=data["to_user"])
            ticket = Ticket.objects.create(
                from_user=request.user, to_user=to_user,
                building=building,
                title=data["title"], message=data["message"]
            )
            return response(status.HTTP_201_CREATED, instance=ticket, serializer=cs.TicketSerializer)


class RetrieveTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        is_for_user = has_obj_permission(request, obj=ticket.to_user)
        is_from_user = has_obj_permission(request, obj=ticket.from_user)
        is_manager_building = has_obj_permission(request, obj=ticket.building.owner)
        if is_for_user or is_from_user or is_manager_building:
            if not ticket.seen and request.user == ticket.to_user:
                ticket.seen = True
                ticket.save()
                ticket.refresh_from_db()
            return response(status.HTTP_200_OK, instance=ticket, serializer=cs.TicketSerializer)
        raise PermissionDenied
