
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction


def entity_payload(instance, *, key=None, extra=None):
    """Return the small, non-sensitive identifier payload used by CRUD events."""
    payload = {key or f"{instance._meta.model_name}_id": instance.pk}
    if hasattr(instance, "school_id") and instance.school_id is not None:
        payload["school_id"] = instance.school_id
    if extra:
        payload.update(extra)
    return payload


def has_relevant_changes(instance, changes):
    """Avoid events for no-op PATCH/PUT requests (including uploaded files)."""
    for field, value in changes.items():
        current = getattr(instance, field)
        if getattr(current, "pk", current) != getattr(value, "pk", value):
            return True
    return False


def publish_event(*, event_type, school_id=None, payload=None):
    """
    Publish a server-generated event to authorized audiences.
    Call only after the database transaction has committed.
    """
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    message = {
        "type": "event.update",
        "payload": {
            "type": event_type,
            "school_id": school_id,
            "data": payload or {},
        },
    }

    async_to_sync(channel_layer.group_send)(
        "eventflow.global",
        message,
    )

    if school_id is not None:
        async_to_sync(channel_layer.group_send)(
            f"eventflow.school.{school_id}",
            message,
        )


def publish_event_on_commit(*, event_type, school_id, payload):
    """Schedule one minimal server event after the surrounding transaction commits."""
    event_payload = dict(payload)
    transaction.on_commit(
        lambda: publish_event(
            event_type=event_type,
            school_id=school_id,
            payload=event_payload,
        )
    )
