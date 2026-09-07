from rest_framework import serializers


def validate_event_points(
    points_1st,
    points_2nd,
    points_3rd,
):

    if points_1st <= points_2nd:

        raise serializers.ValidationError(
            "1st place points must be greater than 2nd place points."
        )

    if points_2nd <= points_3rd:

        raise serializers.ValidationError(
            "2nd place points must be greater than 3rd place points."
        )


def validate_max_participants(
    event_type,
    max_participants,
):

    if (
        event_type == "INDIVIDUAL"
        and max_participants > 1
    ):

        raise serializers.ValidationError(
            "Individual events can have only 1 participant."
        )