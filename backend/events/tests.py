from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from schools.models import School
from .models import Event, EventCategory


class EventValidationTests(APITestCase):
    def setUp(self):
        self.school = School.objects.create(name="Alpha School", code="ALPHA")
        self.other_school = School.objects.create(name="Beta School", code="BETA")
        self.admin = User.objects.create_user(
            username="alpha-admin",
            password="not-a-real-password",
            role=User.Roles.ADMIN,
            school=self.school,
        )
        self.category = EventCategory.objects.create(school=self.school, name="Music")
        self.other_category = EventCategory.objects.create(
            school=self.other_school, name="Dance"
        )
        self.client.force_authenticate(self.admin)

    def payload(self, **overrides):
        data = {
            "school": self.school.id,
            "category": self.category.id,
            "name": "Solo Song",
            "code": "SONG-1",
            "event_type": Event.EventType.INDIVIDUAL,
            "max_participants": 1,
            "points_1st": 10,
            "points_2nd": 5,
            "points_3rd": 3,
        }
        data.update(overrides)
        return data

    def test_category_must_belong_to_event_school(self):
        response = self.client.post(
            "/api/events/",
            self.payload(category=self.other_category.id),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_uses_existing_values_for_validation(self):
        event = Event.objects.create(
            school=self.school,
            category=self.category,
            name="Solo Song",
            code="SONG-1",
            event_type=Event.EventType.INDIVIDUAL,
            max_participants=1,
            points_1st=10,
            points_2nd=5,
            points_3rd=3,
        )

        response = self.client.patch(
            f"/api/events/{event.id}/", {"name": "Updated Solo Song"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Solo Song")
