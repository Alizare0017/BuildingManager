from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import User
from buildings.models import Building, Unit


class ManagerTestCase(TestCase):
    client_class = APIClient
    default_password = "password123"

    @classmethod
    def setUpTestData(cls):
        cls.building_url = reverse("buildings")
        cls.manager = User.objects.create_user(username="testManager", password=cls.default_password, role=User.MANAGER)

    def setUp(self) -> None:
        self.manager_token = Token.objects.get_or_create(user=self.manager)[0].key

    def test_create_new_building(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post(self.building_url, data={"name": "testBuilding", "unit_count": 10})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

