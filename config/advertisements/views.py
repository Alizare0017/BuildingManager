from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework import status

from django.shortcuts import get_object_or_404

from buildings.custom_permission_classes import IsManager
from utils.general import response

from permissions.permissions import has_permission, has_obj_permission
from permissions import filters

from .models import Advertisement
from . import serializers as cs

from buildings.models import Unit


"""
1.The AdvertisementView class is defined as a subclass of APIView.

2.The get method retrieves all Advertisement objects from the database using the all() method of the Advertisement model manager. Then it serializes the retrieved objects using the AdOutSerializer serializer and returns them in the HTTP response with the status code of 200.

3.The post method handles the creation of a new advertisement object based on the data provided in the request body.

4.The code checks if the requesting user has the IS_MANAGER and IS_AUTHENTICATED permissions, and raises an exception if they don't.

5.The AdInSerializer serializer is used to validate the data in the request body. If the data is not valid, the code returns a HTTP 400 bad request response with the errors in the serializer.

6.The code uses the get_object_or_404 function to retrieve the Unit object based on the unit field in the request data, and then retrieves the UnitSpecification associated with the Unit.

7.The code checks if the Unit has a UnitSpecification associated with it, and if not, returns a HTTP 400 bad request response with a detail message.

8.The code uses the has_obj_permission function to check if the requesting user has permission to access the Building object associated with the Unit. If the user doesn't have permission, the code raises an exception.

9.The code creates a new Advertisement object using the validated data and the retrieved UnitSpecification, saves it to the database, and then retrieves it again with the refresh_from_db method.

10.Finally, the code returns a HTTP 201 created response with the serialized advertisement object using the AdOutSerializer.

(Overall, this code appears to be well-organized and handles the creation and retrieval of advertisements in a secure and efficient manner.)
"""
class AdvertisementView(APIView):

    def get(self, request):
        ads = Advertisement.objects.all()
        return response(status.HTTP_200_OK, instance=ads, serializer=cs.AdOutSerializer, many=True)

    def post(self, request):
        has_permission(request, filters.IS_MANAGER, raise_exception=True)
        has_permission(request, filters.IS_AUTHENTICATED, raise_exception=True)

        serializer = cs.AdInSerializer(data=request.data)
        if not serializer.is_valid():
            return response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

        data = dict(serializer.data)
        unit = get_object_or_404(Unit, pk=data.pop("unit"))
        unit_spec = unit.unitspecification
        if not unit_spec:
            return response(status.HTTP_400_BAD_REQUEST, detail="add unit specification firs!")
        has_obj_permission(request, obj=unit.building.owner, raise_exception=True)
        ad = Advertisement.objects.create(**data, unit_specification=unit_spec)
        ad.save()
        ad.refresh_from_db()
        return response(status.HTTP_201_CREATED, instance=ad, serializer=cs.AdOutSerializer)



"""
The view first retrieves the Advertisement instance using the get_object_or_404() shortcut function with the pk parameter passed in the URL. It then checks if the user has the required object-level permission to perform this action by calling the has_obj_permission() function with the request, Advertisement instance's owner, and raise_exception parameters.

If the user has the required permission, the view deletes the Advertisement instance from the database and returns a response with a status code of 204 No Content to indicate that the request has been successful and there is no content to return.
"""
class DestroyAddView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def delete(self, request, pk):
        ad = get_object_or_404(Advertisement, pk=pk)
        has_obj_permission(
            request, obj=ad.unit_specification.unit.building.owner, raise_exception=True)
        ad.delete()
        return response(status.HTTP_204_NO_CONTENT)
