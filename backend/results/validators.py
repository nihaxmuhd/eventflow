from rest_framework import serializers

from .models import Result


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


def validate_result_data(
    school,
    event,
    registration,
    position,
):

    # School validation

    if (
        event.school_id
        != school.id
    ):
        raise serializers.ValidationError(
            (
                "Event must belong "
                "to the selected school."
            )
        )

    if (
        registration.school_id
        != school.id
    ):
        raise serializers.ValidationError(
            (
                "Registration must belong "
                "to the selected school."
            )
        )

    # Registration event validation

    if (
        registration.event_id
        != event.id
    ):
        raise serializers.ValidationError(
            (
                "Registration does not "
                "belong to this event."
            )
        )

    # Position duplicate validation

    existing = Result.objects.filter(
        event=event,
        position=position,
    )

    if existing.exists():

        raise serializers.ValidationError(
            (
                f"Position {position} "
                f"is already assigned."
            )
        )