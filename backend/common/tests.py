import asyncio
from unittest.mock import patch

from channels.testing import WebsocketCommunicator
from django.db import transaction
from django.test import TransactionTestCase
from django.test import override_settings
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User
from core.asgi import application
from schools.models import School
from .realtime import publish_event, publish_event_on_commit


class RealtimeCommitTests(TransactionTestCase):
    def test_event_is_not_published_until_commit_and_is_discarded_on_rollback(self):
        with patch("common.realtime.publish_event") as publish:
            with transaction.atomic():
                publish_event_on_commit(
                    event_type="registration.created",
                    school_id=1,
                    payload={"registration_id": 1},
                )
                publish.assert_not_called()
            publish.assert_called_once_with(
                event_type="registration.created",
                school_id=1,
                payload={"registration_id": 1},
            )

        with patch("common.realtime.publish_event") as publish:
            try:
                with transaction.atomic():
                    publish_event_on_commit(
                        event_type="registration.created",
                        school_id=1,
                        payload={"registration_id": 2},
                    )
                    raise RuntimeError("force rollback")
            except RuntimeError:
                pass
            publish.assert_not_called()


@override_settings(CHANNEL_LAYERS={
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},
})
class RealtimeWebSocketIntegrationTests(TransactionTestCase):
    def setUp(self):
        self.school = School.objects.create(name="Alpha School", code="ALPHA")
        self.other_school = School.objects.create(name="Beta School", code="BETA")
        self.super_admin = User.objects.create_user(
            username="super-admin",
            password="not-a-real-password",
            role=User.Roles.SUPER_ADMIN,
        )
        self.school_admin = User.objects.create_user(
            username="alpha-admin",
            password="not-a-real-password",
            role=User.Roles.ADMIN,
            school=self.school,
        )
        self.other_admin = User.objects.create_user(
            username="beta-admin",
            password="not-a-real-password",
            role=User.Roles.ADMIN,
            school=self.other_school,
        )

    def test_server_event_reaches_only_authorized_subscribers(self):
        async def connect(user):
            socket = WebsocketCommunicator(application, "/ws/events/")
            connected, _ = await socket.connect()
            self.assertTrue(connected)
            self.assertEqual((await socket.receive_json_from())["type"], "auth.required")
            await socket.send_json_to({"type": "auth", "token": str(AccessToken.for_user(user))})
            self.assertEqual((await socket.receive_json_from())["type"], "auth.success")
            return socket

        async def scenario():
            super_socket = await connect(self.super_admin)
            school_socket = await connect(self.school_admin)
            other_socket = await connect(self.other_admin)
            try:
                await asyncio.to_thread(
                    publish_event,
                    event_type="result.created",
                    school_id=self.school.id,
                    payload={"result_id": 42, "event_id": 7, "position": 1, "points": 10},
                )
                for socket in (super_socket, school_socket):
                    message = await socket.receive_json_from(timeout=3)
                    self.assertEqual(message["type"], "event.update")
                    self.assertEqual(message["event"]["type"], "result.created")
                    self.assertEqual(message["event"]["data"], {
                        "result_id": 42, "event_id": 7, "position": 1, "points": 10,
                    })
                self.assertTrue(await other_socket.receive_nothing(timeout=1))
            finally:
                await super_socket.disconnect()
                await school_socket.disconnect()
                await other_socket.disconnect()

        asyncio.run(scenario())
