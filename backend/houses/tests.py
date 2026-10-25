from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from schools.models import School
from students.models import Student
from .models import House


class HouseAuthorizationTests(APITestCase):
    def setUp(self):
        self.school = School.objects.create(name="Alpha School", code="ALPHA")
        self.admin = User.objects.create_user(
            username="alpha-admin",
            password="not-a-real-password",
            role=User.Roles.ADMIN,
            school=self.school,
        )
        self.client.force_authenticate(self.admin)

    def test_admin_can_create_without_client_school(self):
        response = self.client.post(
            "/api/houses/",
            {"name": "Red", "code": "RED", "color": "#ff0000"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["school"], self.school.id)

    def test_house_with_students_cannot_be_deleted(self):
        house = House.objects.create(
            school=self.school, name="Red", code="RED", color="#ff0000"
        )
        Student.objects.create(
            school=self.school,
            house=house,
            admission_number="A-100",
            first_name="Asha",
            gender=Student.Gender.FEMALE,
            class_name="10",
            division="A",
        )

        response = self.client.delete(f"/api/houses/{house.id}/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(House.objects.filter(pk=house.pk).exists())
