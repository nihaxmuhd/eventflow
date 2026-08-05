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

    return Student.objects.create(**data)


def update_student(student, **data):

    validate_admission_number(
        school=data.get("school", student.school),
        admission_number=data.get(
            "admission_number",
            student.admission_number,
        ),
        instance=student,
    )

    validate_student_email(
        school=data.get("school", student.school),
        email=data.get("email", student.email),
        instance=student,
    )

    for field, value in data.items():
        setattr(student, field, value)

    student.save()

    return student


def delete_student(student):

    student.delete()