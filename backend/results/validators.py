from rest_framework import serializers


def validate_position(position):

    if position < 1:

        raise serializers.ValidationError(
            "Position must be greater than zero."
        )


def validate_points(points):

    if points < 0:

        raise serializers.ValidationError(
            "Points cannot be negative."
        )