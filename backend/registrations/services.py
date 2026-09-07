from .models import Registration


def create_registration(
    **data,
):

    return Registration.objects.create(
        **data,
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