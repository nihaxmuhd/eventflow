"""Non-destructive live WebSocket smoke test for a running Daphne server.

It uses an existing active school user and never prints the generated JWT.
Run it only against a development database whose existing accounts are in
scope for testing.
"""

import asyncio
import json
import os
import time

import django
import websockets
from asgiref.sync import sync_to_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from accounts.models import User
from channels.layers import get_channel_layer
from rest_framework_simplejwt.tokens import AccessToken


@sync_to_async
def test_principal():
    user = (
        User.objects.filter(is_active=True, school__isnull=False)
        .order_by("id")
        .first()
    )
    if user is None:
        return None
    return str(AccessToken.for_user(user)), user.school_id


async def receive_json(socket, timeout=10):
    return json.loads(await asyncio.wait_for(socket.recv(), timeout))


async def main():
    principal = await test_principal()
    if principal is None:
        raise RuntimeError("No active school user is available for the live test.")
    token, school_id = principal

    started = time.monotonic()
    async with websockets.connect("ws://127.0.0.1:8001/ws/events/") as socket:
        greeting = await receive_json(socket)
        assert greeting["type"] == "auth.required", greeting

        await socket.send(json.dumps({"type": "auth", "token": token}))
        authenticated = await receive_json(socket)
        assert authenticated["type"] == "auth.success", authenticated

        await get_channel_layer().group_send(
            f"eventflow.school.{school_id}",
            {
                "type": "event.update",
                "payload": {
                    "type": "registration.created",
                    "school_id": school_id,
                    "data": {
                        "registration_id": 999001,
                        "event_id": 999002,
                        "status": "PENDING",
                    },
                },
            },
        )
        event = await receive_json(socket)
        assert event["type"] == "event.update", event

        await asyncio.sleep(max(0, 60 - (time.monotonic() - started)))
        assert socket.state.name == "OPEN", socket.state

    print("Live WebSocket authenticated, delivered one event, and stayed open for 60 seconds.")


if __name__ == "__main__":
    asyncio.run(main())
