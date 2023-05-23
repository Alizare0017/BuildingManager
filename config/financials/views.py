from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404

from utils.general import response, unauthorized
from utils.buildings import count_all_members

from buildings.custom_permission_classes import IsManager

from permissions.permissions import has_obj_permission, has_permission
from permissions import filters

from buildings.models import Building, Unit

from . import serializers as cs
from .models import Bill

from utils.financials import get_expire_date, check_serializer_keys

"""
The view has two methods:

get - Retrieves all the bills for a building. It first checks if the authenticated user has permission to view bills for the given building. If the user has permission, it retrieves all the bills for the building and returns them with a 200 OK status code.
post - Creates a new bill for a building or divides the bill amount among units or members. It first checks if the authenticated user has permission to create a bill for the given building. If the user has permission, it validates the incoming data and creates a new bill instance with the specified amount, created_by, unit (if provided), and expire_date. If a unit is not provided, it divides the bill amount among units or members based on the divide_by field in the incoming data. Finally, it returns the created bill instance(s) with a 201 CREATED status code.
There are two serializer classes used in the view:

NewBillSerializer - Validates incoming data while creating a new bill.
BillSerializer - Serializes bill instances for GET requests.
"""
class BillView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request, pk):
        building = get_object_or_404(Building, pk=pk)
        has_obj_permission(request, obj=building.owner, raise_exception=True)
        bills = Bill.objects.filter(unit__building=building)
        return response(status.HTTP_200_OK, instance=bills, serializer=cs.BillSerializer, many=True)

    def post(self, request, pk):
        serializer = cs.NewBillSerializer(data=request.data)
        if not serializer.is_valid():
            return response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
        building = get_object_or_404(Building, pk=pk)
        has_obj_permission(request, obj=building.owner, raise_exception=True)
        data = serializer.data
        check_serializer_keys(data)
        expire_date = get_expire_date(data)
        created_by = request.user
        amount = data["amount"]
        if unit_pk := data.get("unit"):
            unit = get_object_or_404(Unit, pk=unit_pk)
            if unit.building != building:
                return unauthorized()

            bill = Bill.objects.create(amount=amount, created_by=created_by, unit=unit, expire_date=expire_date)
            bill.save()
            bill.refresh_from_db()
            return response(status.HTTP_201_CREATED, instance=bill, serializer=cs.BillSerializer)
        if divide_by := data.get("divide_by"):
            bills = list()
            units = building.units.all()
            if divide_by == serializer.UNIT:
                amount_per_unit = amount / units.count()
                bills = Bill.objects.bulk_create(
                    [
                        Bill(
                            amount=amount_per_unit, created_by=created_by,
                            unit=u, expire_date=expire_date) for u in units
                    ]
                )
            if divide_by == serializer.MEMBER:
                all_members = count_all_members(units)["all_members"]
                amount_per_member = amount / all_members

                bills = Bill.objects.bulk_create(
                    [
                        Bill(
                            amount=amount_per_member * u.members, created_by=request.user,
                            unit=u, expire_date=expire_date) for u in units
                    ]
                )

            return response(status.HTTP_201_CREATED, instance=bills, serializer=cs.BillSerializer, many=True)

"""
This is a view that handles GET requests for bills that belong to a specific resident. The view filters bills by the user's residence and returns them serialized using BillSerializer.

However, there is no permission class specified, which means that anyone can access this view, including unauthorized users. It might be necessary to add some permission classes to ensure that only authenticated users can access this endpoint.
"""
class ResidentBillsView(APIView):

    def get(self, request):
        if request.user.is_manager:
            return response(status.HTTP_400_BAD_REQUEST, detail=f"use {BillView.__name__}")
        resident_bills = Bill.objects.filter(unit__resident=request.user)
        return response(status.HTTP_200_OK, instance=resident_bills, serializer=cs.BillSerializer, many=True)

"""
It seems that the PaidView API view is used to update a bill as paid by a manager. The view only allows POST requests and requires authentication as well as the IsManager permission.

When a POST request is received, the view first checks if a bill with the given pk exists and belongs to a building owned by the requesting manager. If such a bill is found and it has not been paid already, the view updates the is_paid field of the bill to True and returns a successful response with status code 200. If the bill has already been paid, the view returns a response with status code 400 and a message indicating that the bill has already been paid. If the bill is not found or does not belong to a building owned by the requesting manager, the view returns a response with status code 400 and a message indicating that the bill either not found or it's not for this manager buildings.
"""
class PaidView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request, pk):
        if bill := Bill.objects.filter(pk=pk, unit__building__owner=request.user).first():
            if bill.is_paid:
                return response(status.HTTP_400_BAD_REQUEST, detail="already paid")
            bill.is_paid = True
            bill.save()
            return response(status.HTTP_200_OK, detail="paid")
        return response(
            status.HTTP_400_BAD_REQUEST, detail="bill either not found or its not for this manager buildings")

"""
The RetrieveDestroyView class seems to be an API view for retrieving and deleting a specific bill. Here is a breakdown of its methods:

get: This method is used for retrieving a specific bill instance. It checks whether the user making the request is either the owner of the bill or the owner of the building where the unit associated with the bill is located. If the user has the necessary permissions, the method returns a serialized instance of the bill with a status code of HTTP_200_OK. Otherwise, it returns an unauthorized response with a status code of HTTP_401_UNAUTHORIZED.

delete: This method is used for deleting a specific bill instance. It first checks whether the user making the request is a building manager by calling the has_permission function with the IS_MANAGER filter. If the user has the necessary permissions, it checks whether the bill has already been paid. If the bill has been paid, it returns a bad request response with a status code of HTTP_400_BAD_REQUEST. Otherwise, it deletes the bill and returns a no content response with a status code of HTTP_204_NO_CONTENT.
"""
class RetrieveDestroyView(APIView):

    def get(self, request, pk):
        bill = get_object_or_404(Bill, pk=pk)
        is_bill_owner = has_obj_permission(request, obj=bill.unit.resident)
        is_building_manager = has_obj_permission(request, obj=bill.unit.building.owner)
        if is_bill_owner or is_building_manager:
            return response(status.HTTP_200_OK, instance=bill, serializer=cs.BillSerializer)
        return response(status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        bill = get_object_or_404(Bill, pk=pk)
        has_permission(request, filters.IS_MANAGER, raise_exception=True)

        if bill.is_paid:
            return response(
                status.HTTP_400_BAD_REQUEST, detail="you can't delete a bill that's already has been paid")
        bill.delete()
        return response(status.HTTP_204_NO_CONTENT)
