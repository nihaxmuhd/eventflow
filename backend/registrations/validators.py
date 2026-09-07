from rest_framework import serializers

from .models import Registration


def validate_student_registration(
    student,
    event,
):

    if Registration.objects.filter(
        student=student,
        event=event,
    ).exists():

        raise serializers.ValidationError(
            "Student is already registered for this event."
        )