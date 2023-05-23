from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.models import User
from users.serializers import UserSerializer


class UserTestCase(TestCase):
    client_class = APIClient
    default_password = "password123"

    @classmethod
    def setUpTestData(cls):
        cls.user_url = reverse("users")
        cls.admin_user = User.objects.create(username="testAdmin", password=cls.default_password, is_staff=True)

    def setUp(self):
        self.sample_resident = User.objects.create_user(
            username="testResident", password=self.default_password, role=User.RESIDENT)
        self.sample_manager = User.objects.create_user(
            username="testManager", password=self.default_password, role=User.MANAGER)
        self.sample_resident_token = Token.objects.get_or_create(user=self.sample_resident)[0].key
        self.sample_manager_token = Token.objects.get_or_create(user=self.sample_manager)[0].key
        self.admin_token = Token.objects.get_or_create(user=self.admin_user)[0].key

    def test_user_register(self):
        response = self.client.post(self.user_url,
                                    data={"username": "testUser",
                                          "password": self.default_password})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="testUser")
        serializer = UserSerializer(user)
        self.assertEqual(response.json()["instances"], serializer.data)

    def test_identical_username_registration(self):
        response = self.client.post(self.user_url, data={"username": "testResident", "password": self.default_password})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        response = self.client.post(
            self.user_url + "login/", {"username": self.sample_resident.username, "password": self.default_password}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.json())

    def test_register_and_login(self):
        username = "newUserRegistration"
        password = self.default_password

        response = self.client.post(self.user_url, {"username": username, "password": password})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        login_response = self.client.post(
            self.user_url + "login/", {"username": username, "password": password}
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("token", login_response.json())

    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.sample_resident_token)
        response = self.client.post(self.user_url + "logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token)
        id = self.sample_resident.id
        response = self.client.get(f"{self.user_url}{id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(self.sample_resident)
        self.assertEqual(response.json()["instances"], serializer.data)

    def test_retrieve_user_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.sample_resident_token)
        id = self.sample_resident.id
        response = self.client.get(f"{self.user_url}{id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(self.sample_resident)
        self.assertEqual(response.json()["instances"], serializer.data)

    def test_retrieve_user_by_others(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.sample_resident_token)
        response = self.client.get(f"{self.user_url}{self.admin_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token)
        id = self.sample_resident.id
        response = self.client.delete(f"{self.user_url}{id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaisesMessage(User.DoesNotExist, "User matching query does not exist."):
            User.objects.get(username=self.sample_resident.username)

    def test_delete_account_by_resident(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.sample_resident_token)
        url = reverse("delete_account", kwargs={"pk": self.sample_resident.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_account_by_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.sample_manager_token)
        url = reverse("delete_account", kwargs={"pk": self.sample_manager.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

