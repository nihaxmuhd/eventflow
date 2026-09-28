from rest_framework.exceptions import ValidationError
from django.db.models import ProtectedError

from .models import Student
from .validators import (
    validate_admission_number,
    validate_student_email,
)


def create_student(**data):

    validate_admission_number(
        school=data["school"],
        admission_number=data["admission_number"],
    )

    validate_student_email(
        school=data["school"],
        email=data.get("email"),
    )

    house = data.get("house")

    if house and house.school_id != data["school"].id:
        raise ValidationError(
            {
                "house": (
                    "Selected house does not belong "
                    "to this school."
                )
            }
        )

    return Student.objects.create(**data)


def update_student(student, **data):

    school = data.get(
        "school",
        student.school,
    )

    house = data.get(
        "house",
        student.house,
    )

    if house and house.school_id != school.id:
        raise ValidationError(
            {
                "house": (
                    "Selected house does not belong "
                    "to this school."
                )
            }
        )

    validate_admission_number(
        school=school,
        admission_number=data.get(
            "admission_number",
            student.admission_number,
        ),
        instance=student,
    )

    validate_student_email(
        school=school,
        email=data.get(
            "email",
            student.email,
        ),
        instance=student,
    )

    for field, value in data.items():
        setattr(student, field, value)

    student.save()

    return student


from django.db.models import ProtectedError


def delete_student(student):

    try:
        student.delete()

    except ProtectedError:

        raise ValidationError(
            {
                "student": (
                    "Cannot delete student. "
                    "Related records exist."
                )
            }
        )