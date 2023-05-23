from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.shortcuts import get_object_or_404

from buildings.models import Building

from .models import Announcement
from . import serializers as cs
from utils.general import response

from permissions.permissions import has_obj_permission, has_permission
from permissions import filters




"""
This is a Django REST framework API view for managing announcements related to a building.

permission_classes is set to [IsAuthenticated], which means that only authenticated users can access this view.

The get method takes a pk parameter representing the primary key of the building and returns a list of announcements associated with that building. The list is serialized using cs.AnnouncementSerializer.

The post method also takes a pk parameter representing the primary key of the building. It creates a new announcement associated with that building using cs.AnnouncementSerializer. If the serializer data is not valid, it returns a 400 Bad Request response with the validation errors. Otherwise, it creates the announcement with the building and poster fields set to the specified building and the current user, respectively. It also adds the current user to the seen_by field of the announcement. The created announcement is serialized using cs.AnnouncementSerializer and returned with a 201 Created response.
"""
class AnnouncementsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        building = get_object_or_404(Building, pk=pk)
        announcements = Announcement.objects.filter(building=building)
        return response(status.HTTP_200_OK, instance=announcements, serializer=cs.AnnouncementSerializer, many=True)

    def post(self, request, pk):
        building = get_object_or_404(Building, pk=pk)
        serializer = cs.AnnouncementSerializer(data=request.data)
        if not serializer.is_valid():
            return response(status.HTTP_200_OK, errors=serializer.errors)
        announcement = Announcement.objects.create(**serializer.data, building=building, poster=request.user)
        announcement.seen_by.add(request.user)
        return response(status.HTTP_201_CREATED, instance=announcement, serializer=cs.AnnouncementSerializer)


"""
In the get method, the announcement is retrieved using the given pk and the user who retrieved it is added to the list of seen_by. The AnnouncementSerializer is used to serialize the announcement instance and returned as the response.

In the delete method, the announcement is retrieved using the given pk. If the user who is requesting the deletion has the appropriate permission (i.e. either the poster of the announcement or a manager), the announcement is deleted and a 204 NO CONTENT response is returned. If the user does not have the appropriate permission, a PermissionDenied exception is raised.
"""
class RetrieveDestroyAnnouncementsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        announcement = get_object_or_404(Announcement, pk=pk)
        announcement.seen_by.add(request.user)
        return response(status.HTTP_200_OK, instance=announcement, serializer=cs.AnnouncementSerializer)

    def delete(self, request, pk):
        announcement = get_object_or_404(Announcement, pk=pk)
        if has_obj_permission(request, obj=announcement.poster) or has_permission(request, filters.IS_MANAGER):
            announcement.delete()
            return response(status.HTTP_204_NO_CONTENT)
        raise PermissionDenied
