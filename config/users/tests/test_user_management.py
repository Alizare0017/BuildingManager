from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import User
from users.serializers import UserSerializer


class UserManagementTestCase(TestCase):
    client_class = APIClient
    default_password = "password123"

    @classmethod
    def setUpTestData(cls):
        cls.user_url = reverse("users")

        User.objects.create(username="testUser", password=cls.default_password)
        User.objects.create(username="testUser2", password=cls.default_password)
        User.objects.create(username="testUser3", password=cls.default_password)
        cls.admin = User.objects.create(username="testAdmin", password=cls.default_password, is_staff=True)
        cls.superuser = User.objects.create_superuser(username="superUser", password=cls.default_password)

    def setUp(self) -> None:
        self.admin_token = Token.objects.get_or_create(user=self.admin)[0].key
        self.superuser_token = Token.objects.get_or_create(user=self.superuser)[0].key

    def test_get_user_list(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token)
        response = self.client.get(self.user_url)
        serializer = UserSerializer(User.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["instances"], serializer.data)

    def test_change_active_status_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token)
        user = User.objects.create_user(username="changeRole", password="password")
        url = reverse("change_active", kwargs={"pk": user.id})
        response = self.client.put(url, {"is_active": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.is_active, False)
