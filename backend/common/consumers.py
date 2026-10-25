
import json
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token):
    try:
        validated_token = JWTAuthentication().get_validated_token(token)
        user = JWTAuthentication().get_user(validated_token)

        if not user.is_active:
            return None

        return {
            "id": user.pk,
            "role": user.role,
            "school_id": user.school_id,
        }
    except (InvalidToken, TokenError, User.DoesNotExist):
        return None


class EventFlowConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user_data = None
        self.groups_to_leave = []

        await self.accept()

        await self.send_json({
            "type": "auth.required",
            "message": "Send your JWT access token to authenticate.",
        })

    async def receive_json(self, content, **kwargs):
        if not isinstance(content, dict):
            await self.close(code=4400)
            return

        message_type = content.get("type")

        if not self.user_data:
            if message_type != "auth":
                await self.close(code=4401)
                return

            token = content.get("token")
            if not isinstance(token, str) or not token:
                await self.close(code=4401)
                return

            self.user_data = await get_user_from_token(token)
            if not self.user_data:
                await self.close(code=4401)
                return

            role = self.user_data["role"]
            school_id = self.user_data["school_id"]

            if role == "SUPER_ADMIN":
                self.groups_to_leave = ["eventflow.global"]
                await self.channel_layer.group_add(
                    "eventflow.global", self.channel_name
                )
            elif school_id is not None:
                group_name = f"eventflow.school.{school_id}"
                self.groups_to_leave = [group_name]
                await self.channel_layer.group_add(
                    group_name, self.channel_name
                )
            else:
                await self.close(code=4403)
                return

            await self.send_json({
                "type": "auth.success",
                "user_id": self.user_data["id"],
                "role": role,
                "school_id": school_id,
            })
            return

        # Clients cannot choose groups or publish server events.
        await self.send_json({
            "type": "error",
            "message": "Client publishing is not supported.",
        })

    async def event_update(self, event):
        await self.send_json({
            "type": "event.update",
            "event": event.get("payload", {}),
            "timestamp": timezone.now().isoformat(),
        })

    async def disconnect(self, close_code):
        for group_name in getattr(self, "groups_to_leave", []):
            await self.channel_layer.group_discard(
                group_name, self.channel_name
            )
