from rest_framework import serializers

from .models import (
    Event,
    EventCategory,
)
from .validators import (
    validate_event_points,
    validate_max_participants,
)


class EventCategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = EventCategory

        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):

    class Meta:

        model = Event

        fields = "__all__"

    def validate(self, attrs):

        validate_event_points(
            attrs.get("points_1st"),
            attrs.get("points_2nd"),
            attrs.get("points_3rd"),
        )

        validate_max_participants(
            attrs.get("event_type"),
            attrs.get("max_participants"),
        )

        return attrs