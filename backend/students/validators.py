from rest_framework.exceptions import ValidationError

from .models import Student


def validate_admission_number(
    school,
    admission_number,
    instance=None,
):
    queryset = Student.objects.filter(
        school=school,
        admission_number__iexact=admission_number,
    )

    if instance:
        queryset = queryset.exclude(pk=instance.pk)

    if queryset.exists():
        raise ValidationError(
            {
                "admission_number": (
                    "A student with this admission number "
                    "already exists in this school."
                )
            }
        )


def validate_student_email(
    school,
    email,
    instance=None,
):
    if not email:
        return

    queryset = Student.objects.filter(
        school=school,
        email__iexact=email,
    )

    if instance:
        queryset = queryset.exclude(pk=instance.pk)

    if queryset.exists():
        raise ValidationError(
            {
                "email": (
                    "This email is already used by another "
                    "student in this school."
                )
            }
        )