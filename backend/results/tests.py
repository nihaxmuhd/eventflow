from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from events.models import Event, EventCategory
from registrations.models import Registration
from schools.models import School
from students.models import Student


class ResultRealtimeTests(APITestCase):
    def setUp(self):
        self.school = School.objects.create(name="Alpha School", code="ALPHA")
        self.admin = User.objects.create_user(
            username="alpha-admin", password="not-a-real-password",
            role=User.Roles.ADMIN, school=self.school,
        )
        category = EventCategory.objects.create(school=self.school, name="Music")
        self.event = Event.objects.create(
            school=self.school, category=category, name="Solo Song", code="SONG-1",
            max_participants=10, points_1st=10, points_2nd=5, points_3rd=3,
        )
        student = Student.objects.create(
            school=self.school, admission_number="A-1", first_name="Asha",
            gender=Student.Gender.FEMALE, class_name="10", division="A",
        )
        self.registration = Registration.objects.create(
            school=self.school, student=student, event=self.event, registration_number="REG-1"
        )
        self.client.force_authenticate(self.admin)

    def test_create_update_and_delete_schedule_minimal_events(self):
        with patch("results.views.publish_event_on_commit") as publish:
            created = self.client.post(
                "/api/results/", {"event": self.event.id, "registration": self.registration.id, "position": 1}, format="json"
            )
            self.assertEqual(created.status_code, status.HTTP_201_CREATED)
            result = created.data
            expected = {"result_id": result["id"], "event_id": self.event.id, "registration_id": self.registration.id, "position": 1, "points": 10}
            publish.assert_called_once_with(event_type="result.created", school_id=self.school.id, payload=expected)

            publish.reset_mock()
            updated = self.client.patch(f"/api/results/{result['id']}/", {"remarks": "Verified"}, format="json")
            self.assertEqual(updated.status_code, status.HTTP_200_OK)
            expected["points"] = 10
            publish.assert_called_once_with(event_type="result.updated", school_id=self.school.id, payload=expected)

            publish.reset_mock()
            deleted = self.client.delete(f"/api/results/{result['id']}/")
            self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)
            publish.assert_called_once_with(event_type="result.deleted", school_id=self.school.id, payload=expected)
