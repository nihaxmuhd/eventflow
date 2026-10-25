from rest_framework import serializers

from .models import (
    Event,
    EventCategory,
)
from .validators import (
    validate_event_points,
    validate_max_participants,
    validate_event_category,
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
        instance = self.instance
        points_1st = attrs.get("points_1st", getattr(instance, "points_1st", None))
        points_2nd = attrs.get("points_2nd", getattr(instance, "points_2nd", None))
        points_3rd = attrs.get("points_3rd", getattr(instance, "points_3rd", None))
        event_type = attrs.get("event_type", getattr(instance, "event_type", None))
        max_participants = attrs.get(
            "max_participants", getattr(instance, "max_participants", None)
        )
        school = attrs.get("school", getattr(instance, "school", None))
        category = attrs.get("category", getattr(instance, "category", None))

        validate_event_points(
            points_1st,
            points_2nd,
            points_3rd,
        )

        validate_max_participants(
            event_type,
            max_participants,
        )

        validate_event_category(school, category)

        return attrs
