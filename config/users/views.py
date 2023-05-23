from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from rest_framework.generics import GenericAPIView
from utils.exceptions import BadRequest
from . import serializers as cs, custom_permission_classes as cp
from .models import User
from rest_framework_swagger import renderers

from utils.general import response, unauthorized, logout
from utils.db import update_instance
from utils.otp import check_otp_request
from utils.db import update_unit_member

from permissions import permissions, filters

from buildings.custom_permission_classes import IsManager

from otp.models import OTP
from otp.serializers import OTPSerializer, SendOTPSerializer, OTPVerificationSerializer


class ListRegisterUserView(APIView):
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer,
    ]
    permission_classes = [cp.ListUserPermission]

    def get(self, request):
        """
        only staff
        """
        users = User.objects.all()
        return response(
            status.HTTP_200_OK, instance=users, serializer=cs.UserSerializer, total=users.count(), many=True)

    def post(self, request):
        serializer = cs.RegisterUserSerializer(data=request.data)

        if serializer.is_valid():
            try:
                building_manager = User.objects.create_user(**serializer.data, role=User.MANAGER)
            except IntegrityError as e:
                return response(status.HTTP_400_BAD_REQUEST, errors=str(e))
            return response(status.HTTP_201_CREATED, instance=building_manager, serializer=cs.UserSerializer)
        return response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)


class LoginView(APIView):

    def post(self, request, format=None):

        serializer = cs.LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return response(errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        data = serializer.data

        user = get_object_or_404(User, username=data.get("username"))
        if not user.is_active:
            return unauthorized()

        if not user.check_password(data.get("password")):
            return response(
                detail="provided username and password dont match",
                errors="wrong_credentials", status_code=status.HTTP_401_UNAUTHORIZED
            )
        login(request, user)
        token = Token.objects.get_or_create(user=user)
        return response(
            detail=f"{user.username} logged in successfully",
            status_code=status.HTTP_200_OK, token=token[0].key
        )


class LogoutView(APIView):

    def post(self, request, format=None):
        logout(request)
        return response(detail="Successfully logged out", status_code=status.HTTP_200_OK)


class RetrieveUpdateDestroyUserView(APIView):
    permission_classes = [cp.DestroyUserPermission]

    def get(self, request, pk):
        if permissions.has_permission(request, filters.IS_STAFF) or permissions.has_obj_permission(request, pk=pk):
            user = get_object_or_404(User, pk=pk)
            return response(status.HTTP_200_OK, instance=user, serializer=cs.UserSerializer)
        raise PermissionDenied

    def put(self, request, pk):
        permissions.has_obj_permission(request, pk=pk, raise_exception=True)
        serializer = cs.UpdateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            data = dict(serializer.data)
            if "members" in data:
                members = data.pop("members")
                update_unit_member(request, members)

            update_instance(user, data)
            user.refresh_from_db()
            return response(status.HTTP_200_OK, instance=user, serializer=cs.UserSerializer)
        return response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        logout(request)
        user.delete()
        return response(status.HTTP_204_NO_CONTENT)


class ChangeActiveStatusView(APIView):
    """
    turn a user active status to de-active and vice-versa
    """

    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        serializer = cs.ChangeActiveStatusSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, pk=pk)
            update_instance(user, serializer.data)
            return response(status_code=status.HTTP_200_OK)
        return response(status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)


class DeleteAccountView(APIView):
    """
    only account owner them-self can use this views. mods can ChangeActiveStatusView to ban/unban users
    """
    permission_classes = [IsManager]

    def post(self, request, pk):
        if permissions.has_obj_permission(request, pk=pk, raise_exception=True):
            request.user.is_active = False
            request.user.save()
            request.user.auth_token.delete()
            logout(request)
            return response(status.HTTP_200_OK)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return response(status.HTTP_200_OK, instance=request.user, serializer=cs.UserSerializer)


class SendVerificationView(APIView):
    """
    this view handle sending OTP for email and phone verification.
    we should implement sending the OTP via email or phone but for now we just show a json response
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        permissions.has_obj_permission(request, pk=pk, raise_exception=True)
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

        have_requirement, requirement = check_otp_request(request.user, serializer.data)
        if not have_requirement:
            return response(status.HTTP_400_BAD_REQUEST, detail=f"you need to add {requirement} first")
        if check_otp_request(request.user, serializer.data, check_for_is_active=True):
            return response(status.HTTP_400_BAD_REQUEST, detail=f"{requirement} already activated")
        otp = OTP.objects.get_or_create(request.user, otp_for=serializer.data["otp_for"])
        context = {'otp':otp.code}
        html_message = render_to_string('templates/users/otp_email.html', context)
        email_subject = 'Your OTP'
        email_body = strip_tags(html_message)
        sender_email = settings.DEFAULT_FROM_EMAIL
        print(sender_email)
        user = User.objects.filter(pk=pk)
        print(user)
        to_email = [user[0].email]
        send_mail(email_subject, email_body, sender_email, to_email,html_message=html_message)

        return response(status.HTTP_201_CREATED, instance=otp, serializer=OTPSerializer)



class VerificationView(APIView):
    """
    this view handle verifying OTP for email and phone verification.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        permissions.has_obj_permission(request, pk=pk)
        serializer = OTPVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            return response(status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
        otp_for = serializer.data["otp_for"]
        otp = OTP.objects.filter(user=request.user, otp_for=otp_for).last()
        if not otp:
            raise BadRequest(detail="wrong code")
        if otp.is_expired or otp.used:
            return response(status.HTTP_400_BAD_REQUEST, detail="otp expired or already used")
        update_instance(request.user, {f"is_{otp_for.lower()}_activated": True})
        otp.burn()
        return response(status.HTTP_200_OK, detail=f"{serializer.data['otp_for'].lower()} verified")
