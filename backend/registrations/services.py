from django.utils import timezone

from .models import Registration


def generate_registration_number():

    year = timezone.now().year

    last_registration = (
        Registration.objects
        .order_by("-id")
        .first()
    )

    next_id = 1

    if last_registration:
        next_id = (
            last_registration.id + 1
        )

    return (
        f"REG-{year}-{next_id:04d}"
    )


def create_registration(
    **data,
):

    data[
        "registration_number"
    ] = generate_registration_number()

    return Registration.objects.create(
        **data
    )


def update_registration(
    registration,
    **data,
):

    for field, value in data.items():

        setattr(
            registration,
            field,
            value,
        )

    registration.save()

    return registration


def delete_registration(
    registration,
):

    registration.delete()