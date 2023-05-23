from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404

from . import serializers as cs
from .custom_permission_classes import IsManager

from .models import Unit, Building, UnitSpecification

from users.models import User

from utils import helper
from utils.general import response
from utils.db import update_instance
from utils.buildings import get_all_residents

from permissions.permissions import has_obj_permission, has_permission
from permissions import filters

from . import custom_permission_classes as cp


class BuildingView(APIView):
    permission_classes = [cp.IsStaffOrManager]

    def get(self, request):
        """
        only staff
        """
        buildings = Building.objects.all()
        return response(status.HTTP_200_OK, instance=buildings, serializer=cs.BuildingSerializer, many=True)

    def post(self, request):
        """
        only managers
        """
        residents_info = list()
        residents = list()
        serializer = cs.CreateBuildingSerializer(data=request.data)
        if serializer.is_valid():
            building = Building.objects.create(**serializer.data, owner=request.user)
        else:
            return response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
        for unit in range(building.unit_count):
            username = helper.random_username(building)
            password = helper.generate_random_password(10)
            residents.append(User.objects.create_user(username=username, password=password, role=User.RESIDENT))
            residents_info.append({"unit": unit + 1, "username": username, "password": password})
        Unit.objects.bulk_create(
            [Unit(
                building=building,
                unit_number=u + 1,
                resident=r)
                for u, r in enumerate(residents)])
        return response(
            status.HTTP_201_CREATED, instance=building, serializer=cs.BuildingSerializer, residents_info=residents_info)


class ManagerBuildingListView(APIView):
    permission_classes = [cp.IsManager]

    def get(self, request):
        manager_buildings = Building.objects.filter(owner=request.user)
        return response(status.HTTP_200_OK, instance=manager_buildings,
                        serializer=cs.BuildingSerializer, many=True,
                        total=manager_buildings.count())


class RetrieveUpdateDestroyBuildingView(APIView):
    permission_classes = [cp.IsManager]

    def get(self, request, pk):
        building = get_object_or_404(Building, pk=pk)
        has_obj_permission(request, obj=building.owner, raise_exception=True)
        return response(status.HTTP_200_OK, instance=building, serializer=cs.BuildingSerializer)

    def put(self, request, pk):
        building = get_object_or_404(Building, pk=pk)
        has_obj_permission(request, obj=building.owner, raise_exception=True)
        serializer = cs.UpdateBuildingSerializer(data=request.data)
        if serializer.is_valid():
            update_instance(building, serializer.data)
            building.refresh_from_db()
            return response(status.HTTP_200_OK, instance=building, serializer=cs.BuildingSerializer)
        return response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def delete(self, request, pk):
        building = get_object_or_404(Building, pk=pk)
        has_obj_permission(request, obj=building.owner, raise_exception=True)
        building.delete()
        return response(status.HTTP_204_NO_CONTENT)


class BuildingsUnitsView(APIView):
    permission_classes = [cp.IsManager]

    def get(self, request, pk):
        building = get_object_or_404(Building, pk=pk)
        has_obj_permission(request, obj=building.owner, raise_exception=True)
        units = building.units.all()
        return response(status.HTTP_200_OK, instance=units, serializer=cs.UnitSerializer, many=True)


class UnitsResidentView(APIView):
    permission_classes = [cp.IsManager]

    def get(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        has_obj_permission(request, obj=unit.building.owner, raise_exception=True)
        return response(status.HTTP_200_OK, instance=unit.resident, serializer=cs.ResidentSerializer)

    def post(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        has_obj_permission(request, obj=unit.building.owner, raise_exception=True)
        building = unit.building
        if not unit.resident:
            username = helper.random_username(building)
            password = helper.generate_random_password(10)
            unit.resident = User.objects.create_user(username=username, password=password)
            unit.save()
            unit.refresh_from_db()
            return response(status.HTTP_201_CREATED,
                            instance=unit,
                            serializer=cs.UnitSerializer,
                            resident_info=(username, password))
        return response(status.HTTP_400_BAD_REQUEST, detail="unit already have a resident")

    def delete(self, request, pk):
        """
        this methode will delete a resident user and set the resident field to None
        """
        unit = get_object_or_404(Unit, pk=pk)
        has_obj_permission(request, obj=unit.building.owner, raise_exception=True)
        resident = unit.resident
        unit.resident = None
        resident.delete()
        unit.save()
        return response(status.HTTP_204_NO_CONTENT, detail="resident deleted")


class GetAllResidentsView(APIView):
    """
    a list of all residents in a building
    """
    permission_classes = [cp.IsManager]

    def get(self, request, pk):
        building = get_object_or_404(Building, pk=pk)
        has_obj_permission(request, obj=building.owner, raise_exception=True)
        residents = get_all_residents(building)
        return response(status.HTTP_200_OK, instance=residents[0],
                        serializer=cs.ResidentSerializer, many=True, all_members=residents[1].pop("all_members"))


class RetrieveUnitView(APIView):

    def get(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        if has_obj_permission(request, obj=unit.building.owner) or has_permission(request, filters.IS_MANAGER):
            resident = cs.ResidentSerializer(unit.resident)
            return response(status.HTTP_200_OK, instance=unit, serializer=cs.UnitSerializer, resident=resident.data)
        raise PermissionDenied


class UnitSpecificationView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):

        serializer = cs.UnitSpecificationSerializer(data=request.data)
        if not serializer.is_valid():
            return response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

        data = dict(serializer.data)
        unit = get_object_or_404(Unit, pk=data["unit"])
        has_obj_permission(request, obj=unit.building.owner, raise_exception=True)
        if UnitSpecification.objects.filter(unit=unit).exists():
            return response(status.HTTP_400_BAD_REQUEST, detail="unit specification already exist")
        data["unit"] = unit
        unit_spec = UnitSpecification.objects.create(**data)
        unit_spec.save()
        unit_spec.refresh_from_db()
        return response(status.HTTP_201_CREATED, instance=unit_spec, serializer=cs.UnitSpecificationSerializer)


class RetrieveUpdateUnitSpecificationView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        has_obj_permission(request, obj=unit.building.owner)
        unit_spec = unit.unitspecification
        return response(status.HTTP_200_OK, instance=unit_spec, serializer=cs.UnitSpecificationSerializer)

    def delete(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        has_obj_permission(request, obj=unit.building.owner)
        unit_spec = unit.unitspecification
        unit_spec.delete()
        return response(status.HTTP_204_NO_CONTENT)