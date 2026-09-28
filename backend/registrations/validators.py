from rest_framework import serializers

from .models import Registration


def validate_student_registration(
    student,
    event,
):

    # Same school validation

    if (
        student.school_id
        != event.school_id
    ):
        raise serializers.ValidationError(
            (
                "Student and Event "
                "must belong to the "
                "same school."
            )
        )

    # Duplicate registration

    if Registration.objects.filter(
        student=student,
        event=event,
    ).exists():

        raise serializers.ValidationError(
            (
                "Student is already "
                "registered for "
                "this event."
            )
        )

    # Capacity validation

    if (
        hasattr(
            event,
            "max_participants",
        )
        and event.max_participants
    ):

        current_count = (
            Registration.objects.filter(
                event=event
            ).count()
        )

        if (
            current_count
            >= event.max_participants
        ):

            raise serializers.ValidationError(
                (
                    "Event participant "
                    "limit reached."
                )
            )