from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from events.models import Event, EventCategory
from schools.models import School
from students.models import Student


class RegistrationRealtimeTests(APITestCase):
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
        self.student = Student.objects.create(
            school=self.school, admission_number="A-1", first_name="Asha",
            gender=Student.Gender.FEMALE, class_name="10", division="A",
        )
        self.client.force_authenticate(self.admin)

    def test_create_update_and_delete_schedule_minimal_events(self):
        with patch("registrations.views.publish_event_on_commit") as publish:
            created = self.client.post(
                "/api/registrations/",
                {"student": self.student.id, "event": self.event.id},
                format="json",
            )
            self.assertEqual(created.status_code, status.HTTP_201_CREATED)
            registration = created.data["data"]
            publish.assert_called_once_with(
                event_type="registration.created", school_id=self.school.id,
                payload={"registration_id": registration["id"], "event_id": self.event.id, "status": "PENDING"},
            )

            publish.reset_mock()
            updated = self.client.patch(
                f"/api/registrations/{registration['id']}/", {"status": "APPROVED"}, format="json"
            )
            self.assertEqual(updated.status_code, status.HTTP_200_OK)
            publish.assert_called_once_with(
                event_type="registration.updated", school_id=self.school.id,
                payload={"registration_id": registration["id"], "event_id": self.event.id, "status": "APPROVED"},
            )

            publish.reset_mock()
            deleted = self.client.delete(f"/api/registrations/{registration['id']}/")
            self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)
            publish.assert_called_once_with(
                event_type="registration.deleted", school_id=self.school.id,
                payload={"registration_id": registration["id"], "event_id": self.event.id, "status": "APPROVED"},
            )
