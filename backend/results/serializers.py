from rest_framework import serializers

from .models import Result
from .validators import (
    validate_position,
    validate_points,
)


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = "__all__"

    def validate(self, attrs):

        validate_position(
            attrs.get("position")
        )

        validate_points(
            attrs.get("points")
        )

        return attrs