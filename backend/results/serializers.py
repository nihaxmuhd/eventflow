from rest_framework import serializers

from .models import Result
from .validators import validate_position


class ResultSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Result

        fields = "__all__"

        read_only_fields = [
            "points",
        ]

    def validate(self, attrs):

        validate_position(
            attrs.get("position")
        )

        return attrs

    def create(self, validated_data):

        event = validated_data["event"]

        position = validated_data["position"]

        points = 0

        if position == 1:
            points = event.points_1st

        elif position == 2:
            points = event.points_2nd

        elif position == 3:
            points = event.points_3rd

        validated_data["points"] = points

        return super().create(
            validated_data
        )

    def update(
        self,
        instance,
        validated_data,
    ):

        event = validated_data.get(
            "event",
            instance.event,
        )

        position = validated_data.get(
            "position",
            instance.position,
        )

        points = 0

        if position == 1:
            points = event.points_1st

        elif position == 2:
            points = event.points_2nd

        elif position == 3:
            points = event.points_3rd

        validated_data["points"] = points

        return super().update(
            instance,
            validated_data,
        )