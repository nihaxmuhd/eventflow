from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from houses.models import House
from schools.models import School
from .models import Student


class StudentCreateAuthorizationTests(APITestCase):
    def setUp(self):
        self.school = School.objects.create(name="Alpha School", code="ALPHA")
        self.other_school = School.objects.create(name="Beta School", code="BETA")
        self.admin = User.objects.create_user(
            username="alpha-admin",
            password="not-a-real-password",
            role=User.Roles.ADMIN,
            school=self.school,
        )
        self.other_house = House.objects.create(
            school=self.other_school,
            name="Beta House",
            code="BETA-H",
            color="#123456",
        )
        self.client.force_authenticate(self.admin)

    def payload(self, **overrides):
        data = {
            "admission_number": "A-100",
            "first_name": "Asha",
            "last_name": "Test",
            "gender": Student.Gender.FEMALE,
            "class_name": "10",
            "division": "A",
        }
        data.update(overrides)
        return data

    def test_admin_can_create_without_client_school(self):
        response = self.client.post("/api/students/", self.payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["school"], self.school.id)

    def test_admin_cannot_create_student_in_another_schools_house(self):
        response = self.client.post(
            "/api/students/",
            self.payload(admission_number="A-101", house=self.other_house.id),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("house", response.data)

    def test_duplicate_email_and_admission_number_return_field_errors(self):
        Student.objects.create(school=self.school, admission_number="A-099", first_name="Existing", gender=Student.Gender.FEMALE, class_name="10", division="A", email="existing@example.com")
        email_response = self.client.post("/api/students/", self.payload(email="existing@example.com"), format="json")
        admission_response = self.client.post("/api/students/", self.payload(admission_number="A-099"), format="json")
        self.assertEqual(email_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(email_response.data["email"], ["A student with this email address already exists."])
        self.assertEqual(admission_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(admission_response.data["admission_number"], ["A student with this admission number already exists."])

    def test_missing_and_unknown_foreign_key_fields_return_drf_field_errors(self):
        missing_response = self.client.post("/api/students/", {"gender": Student.Gender.FEMALE}, format="json")
        invalid_house_response = self.client.post("/api/students/", self.payload(house=999999), format="json")
        self.assertEqual(missing_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("admission_number", missing_response.data)
        self.assertEqual(invalid_house_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("house", invalid_house_response.data)
